import requests
from bs4 import BeautifulSoup
import time
import json
import re
from typing import List, Dict, Any
from fake_useragent import UserAgent
import logging
import os

class RobotScraper:
    def __init__(self):
        # Initialize session with a random User-Agent to minimize blocking
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        self.robots_data: List[Dict[str, Any]] = []
        self.visited_urls: set = set()

    def search_robots(self, search_terms: List[str]) -> List[Dict[str, Any]]:
        all_robots = []
        for term in search_terms:
            print(f"Searching for: {term}")
            robots = self._search_wikipedia(term)
            all_robots.extend(robots)
            time.sleep(1)  # Respectful delay between search terms
        return all_robots

    def _search_wikipedia(self, search_term: str) -> List[Dict[str, Any]]:
        robots = []
        # Define pages to search for robot links
        search_urls = [
            "https://en.wikipedia.org/wiki/Category:Robots",
            "https://en.wikipedia.org/wiki/List_of_robots",
            "https://en.wikipedia.org/wiki/Category:Industrial_robots",
            "https://en.wikipedia.org/wiki/Category:Service_robots"
        ]
        # Prefixes to identify invalid or irrelevant links
        invalid_prefixes = [
            '/wiki/Category:', '/wiki/Help:', '/wiki/Template:',
            '/wiki/List_of_', '/wiki/Portal:', '/wiki/Special:', '/wiki/Talk:'
        ]
        for url in search_urls:
            try:
                response = self.session.get(url)
                if response.status_code != 200:
                    logging.warning(f"Failed to retrieve {url} (status code {response.status_code})")
                    continue
                soup = BeautifulSoup(response.content, 'html.parser')
                # If the page is a list of robots, handle differently
                if "List_of_" in url:
                    robots_list = self._extract_robot_links_from_list_page(soup)
                    robots.extend(robots_list)
                    # small delay to avoid rapid requests
                    time.sleep(0.5)
                    continue
                # For category pages, extract all relevant links
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    if not href.startswith('/wiki/') or href in self.visited_urls:
                        continue
                    if any(href.startswith(prefix) for prefix in invalid_prefixes):
                        continue
                    title = link.get_text().strip()
                    # Adding all candidate robot pages (assuming relevance in category)
                    self.visited_urls.add(href)
                    robot_info = self._extract_robot_info(href, title)
                    if robot_info:
                        robots.append(robot_info)
                        # Pause briefly after each page fetch
                        time.sleep(0.5)
            except Exception as e:
                logging.error(f"[ERROR] {url}: {e}")
        return robots

    def _extract_robot_links_from_list_page(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        robots = []
        # The list page might have multiple sections of lists
        links = soup.select('ul li a[href^="/wiki/"]')
        invalid_prefixes = [
            '/wiki/Category:', '/wiki/Help:', '/wiki/Template:',
            '/wiki/List_of_', '/wiki/Portal:', '/wiki/Special:', '/wiki/Talk:'
        ]
        for link in links:
            href = link['href']
            title = link.get_text().strip()
            if href in self.visited_urls:
                continue
            if any(href.startswith(prefix) for prefix in invalid_prefixes):
                continue
            # We assume all links on the list page are relevant robot pages
            self.visited_urls.add(href)
            robot_info = self._extract_robot_info(href, title)
            if robot_info:
                robots.append(robot_info)
                time.sleep(0.5)
        return robots

    def _is_robot_related(self, title: str, search_term: str) -> bool:
        # Determine if the title is related to robots or matches search term
        keywords = ['robot', 'robotic', 'automation', 'automated', 'humanoid', 'android']
        title_lower = title.lower()
        search_lower = search_term.lower()
        return any(k in title_lower for k in keywords) or search_lower in title_lower

    def _is_strong_robot_name(self, title: str) -> bool:
        # Strong indicators that the title is specifically a robot name
        title_lower = title.lower()
        return any(sub in title_lower for sub in ['robot', 'bot', 'android', 'automaton'])

    def _extract_robot_info(self, wiki_url: str, title: str) -> Dict[str, Any]:
        try:
            # Construct full URL if needed
            full_url = f"https://en.wikipedia.org{wiki_url}" if wiki_url.startswith('/wiki/') else wiki_url
            response = self.session.get(full_url)
            if response.status_code != 200:
                logging.warning(f"Failed to retrieve page {full_url} (status code {response.status_code})")
                return None
            soup = BeautifulSoup(response.content, 'html.parser')
            # Remove Wikipedia citation references in content to clean text
            for sup in soup.find_all('sup'):
                # Remove any citation references or [citation needed] markers
                if sup.get('class') and ('reference' in sup.get('class') or 'Template-Fact' in sup.get('class') or 'Inline-Template' in sup.get('class')):
                    sup.decompose()
            robot_info: Dict[str, Any] = {
                'name': title,
                'url': full_url,
                'description': '',
                'manufacturer': '',
                'year': '',
                'applications': []
            }
            # Extract first meaningful paragraph as description
            content = soup.find('div', {'id': 'mw-content-text'})
            if content:
                paragraphs = content.find_all('p')
                for p in paragraphs:
                    text = p.get_text().strip()
                    # Ensure the paragraph has some content and length > 50 characters
                    if text and len(text) > 50:
                        # Strip any citation or wiki markup artifacts from text
                        # (Already removed <sup> references; remove leftover bracketed notations if any)
                        text_clean = re.sub(r'\[.*?\]', '', text)
                        robot_info['description'] = text_clean if len(text_clean) <= 500 else text_clean[:500] + '...'
                        break
            # If no valid description found, consider this page invalid and skip
            if not robot_info['description']:
                return None
            # Extract infobox data for manufacturer, year, and applications
            infobox = soup.find('table', {'class': 'infobox'})
            if infobox:
                rows = infobox.find_all('tr')
                for row in rows:
                    header = row.find('th')
                    value_cell = row.find('td')
                    if not header or not value_cell:
                        continue
                    key = header.get_text().strip().lower()
                    value_text = value_cell.get_text().strip()
                    # Remove any citation numbers from infobox values
                    value_text = re.sub(r'\[.*?\]', '', value_text)
                    if 'manufacturer' in key:
                        robot_info['manufacturer'] = value_text
                    elif 'year' in key or 'introduced' in key:
                        robot_info['year'] = value_text
                    elif 'application' in key or 'use' in key:
                        # Some infoboxes might list multiple applications separated by newline or comma
                        # Split by common separators and extend the list
                        parts = re.split(r';|,|/|\n', value_text)
                        for part in parts:
                            part_clean = part.strip()
                            if part_clean:
                                robot_info['applications'].append(part_clean)
            # Ensure applications is a list (even if no entries, it remains empty list)
            return robot_info
        except Exception as e:
            logging.error(f"Error extracting from {wiki_url}: {e}")
            return None

    def save_data(self, filename: str = 'robots_data.json'):
        os.makedirs('./data', exist_ok=True)
        with open(f'./data/{filename}', 'w', encoding='utf-8') as f:
            json.dump(self.robots_data, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(self.robots_data)} robots to {filename}")

if __name__ == "__main__":
    scraper = RobotScraper()
    # Search terms help ensure broad coverage of robot pages
    search_terms = [
        "industrial robots", "service robots", "humanoid robots",
        "medical robots", "military robots", "domestic robots",
        "educational robots"
    ]
    robots = scraper.search_robots(search_terms)
    scraper.robots_data = robots
    scraper.save_data()
    print(f"Found {len(robots)} robots.")
