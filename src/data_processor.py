#!/usr/bin/env python3
"""
Enhanced Data Processor for Robot Taxonomy
Enhanced robot classification data processor
Supports time series analysis, regional analysis, trend prediction and other functions
"""

import json
import pandas as pd
import numpy as np
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class RobotDataProcessor:
    def __init__(self, data_path="data/"):
        """Initialize data processor"""
        self.data_path = data_path
        self.robots_data = self.load_robots_data()
        self.features_data = self.load_features_data()
        self.dict_data = self.load_dict_data()
        self.family_index = self.load_family_index()
        
        # Region mapping
        self.region_mapping = {
            'US': 'United States', 'JP': 'Japan', 'DE': 'Germany', 'SE': 'Sweden',
            'CN': 'China', 'UK': 'United Kingdom', 'FR': 'France', 'IT': 'Italy',
            'CA': 'Canada', 'DK': 'Denmark', 'CH': 'Switzerland', 'ES': 'Spain',
            'IL': 'Israel', 'AU': 'Australia', 'KR': 'South Korea', 'IN': 'India',
            'UN': 'Unknown/International', 'EU': 'European Union', 'ZA': 'South Africa',
            'LE': 'Lebanon', 'TW': 'Taiwan', 'PA': 'Pakistan', 'IR': 'Iran',
            'PL': 'Poland', 'BE': 'Belgium', 'PE': 'Peru', 'JA': 'Japan (Alt)',
            'SW': 'Sweden (Alt)'
        }
        
        # Create dataframe
        self.df = self.create_dataframe()

    def load_robots_data(self):
        """Load robot data"""
        robots = []
        try:
            with open(f"{self.data_path}robots.ndjson", 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        robots.append(json.loads(line))
            return robots
        except Exception as e:
            print(f"Failed to load robot data: {e}")
            return []

    def load_features_data(self):
        """Load features data"""
        try:
            with open(f"{self.data_path}features.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load features data: {e}")
            return {}

    def load_dict_data(self):
        """Load dictionary data"""
        try:
            with open(f"{self.data_path}dict.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load dictionary data: {e}")
            return {}

    def load_family_index(self):
        """Load family index"""
        try:
            with open(f"{self.data_path}family_index.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load family index: {e}")
            return {}

    def create_dataframe(self):
        """Create pandas dataframe"""
        data = []
        
        for robot in self.robots_data:
            # Basic information
            row = {
                'id': robot['id'],
                'name': robot['n'],
                'year': robot.get('yr', 0),
                'region_code': robot.get('rg', 'UN'),
                'region_name': self.region_mapping.get(robot.get('rg', 'UN'), robot.get('rg', 'UN')),
                'url': robot.get('url', ''),
                'domain_id': robot.get('d', -1),
                'class_id': robot.get('c', -1),
                'order_id': robot.get('o', -1),
                'primary_role_id': robot.get('pr', -1)
            }
            
            # Classification information
            if robot.get('d', -1) >= 0 and robot['d'] < len(self.dict_data.get('domain', [])):
                row['domain'] = self.dict_data['domain'][robot['d']]
            else:
                row['domain'] = 'Unknown'
                
            if robot.get('c', -1) >= 0 and robot['c'] < len(self.dict_data.get('class', [])):
                row['class'] = self.dict_data['class'][robot['c']]
            else:
                row['class'] = 'Unknown'
                
            # Get order information
            if row['class'] in self.dict_data.get('order_by_class', {}):
                orders = self.dict_data['order_by_class'][row['class']]
                if robot.get('o', -1) >= 0 and robot['o'] < len(orders):
                    row['order'] = orders[robot['o']]
                else:
                    row['order'] = 'Unknown'
            else:
                row['order'] = 'Unknown'
                
            # Primary role
            if robot.get('pr', -1) >= 0 and robot['pr'] < len(self.dict_data.get('primary_role', [])):
                row['primary_role'] = self.dict_data['primary_role'][robot['pr']]
            else:
                row['primary_role'] = 'Unknown'
                
            # Sector information
            sectors = robot.get('tags', {}).get('sector', [])
            if sectors and len(sectors) > 0:
                sector_id = sectors[0]
                if sector_id < len(self.dict_data.get('sector', [])):
                    row['sector'] = self.dict_data['sector'][sector_id]
                else:
                    row['sector'] = 'Unknown'
            else:
                row['sector'] = 'Unknown'
            
            # Feature information
            if str(robot['id']) in {str(item['id']): item for item in self.features_data.get('features', [])}:
                features_info = {str(item['id']): item for item in self.features_data.get('features', [])}[str(robot['id'])]
                row['feature_indices'] = features_info.get('feat', [])
                
                # Extract specific features
                vocab = self.features_data.get('vocab', [])
                row['features'] = [vocab[i] for i in features_info.get('feat', []) if i < len(vocab)]
            else:
                row['feature_indices'] = []
                row['features'] = []
            
            data.append(row)
        
        return pd.DataFrame(data)

    def analyze_temporal_trends(self):
        """Analyze temporal trends"""
        # Filter valid years
        valid_years = self.df[self.df['year'] > 0]
        
        # Statistics by year
        yearly_stats = valid_years.groupby('year').agg({
            'id': 'count',
            'domain': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Unknown',
            'class': lambda x: list(x.unique()),
            'region_name': lambda x: list(x.unique())
        }).rename(columns={'id': 'count'})
        
        # Calculate growth rate
        yearly_stats['growth_rate'] = yearly_stats['count'].pct_change() * 100
        
        # Calculate cumulative count
        yearly_stats['cumulative'] = yearly_stats['count'].cumsum()
        
        return yearly_stats

    def analyze_regional_patterns(self):
        """Analyze regional patterns"""
        regional_analysis = {}
        
        # Basic statistics
        regional_stats = self.df.groupby('region_name').agg({
            'id': 'count',
            'year': ['min', 'max', 'mean'],
            'domain': lambda x: list(x.unique()),
            'class': lambda x: list(x.unique()),
            'sector': lambda x: list(x.unique())
        })
        
        regional_stats.columns = ['count', 'first_year', 'latest_year', 'avg_year', 'domains', 'classes', 'sectors']
        regional_analysis['stats'] = regional_stats
        
        # Regional specialization analysis
        specialization = {}
        for region in self.df['region_name'].unique():
            region_data = self.df[self.df['region_name'] == region]
            class_dist = region_data['class'].value_counts(normalize=True)
            sector_dist = region_data['sector'].value_counts(normalize=True)
            
            specialization[region] = {
                'dominant_class': class_dist.index[0] if len(class_dist) > 0 else 'Unknown',
                'class_diversity': len(class_dist),
                'dominant_sector': sector_dist.index[0] if len(sector_dist) > 0 else 'Unknown',
                'sector_diversity': len(sector_dist)
            }
        
        regional_analysis['specialization'] = specialization
        
        return regional_analysis

    def perform_clustering_analysis(self):
        """Perform clustering analysis"""
        # Prepare feature matrix
        feature_matrix = []
        robot_ids = []
        
        vocab_size = len(self.features_data.get('vocab', []))
        
        for _, robot in self.df.iterrows():
            # Create one-hot encoded feature vector
            feature_vector = [0] * vocab_size
            for feat_idx in robot['feature_indices']:
                if feat_idx < vocab_size:
                    feature_vector[feat_idx] = 1
            
            # Add other features
            feature_vector.extend([
                robot['domain_id'],
                robot['class_id'],
                robot['order_id'],
                robot['primary_role_id'],
                robot['year'] if robot['year'] > 0 else 2000
            ])
            
            feature_matrix.append(feature_vector)
            robot_ids.append(robot['id'])
        
        # Standardization
        scaler = StandardScaler()
        feature_matrix_scaled = scaler.fit_transform(feature_matrix)
        
        # PCA dimensionality reduction
        pca = PCA(n_components=min(10, len(feature_matrix_scaled[0])))
        feature_matrix_pca = pca.fit_transform(feature_matrix_scaled)
        
        # K-means clustering
        n_clusters = min(8, len(feature_matrix_pca))
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(feature_matrix_pca)
        
        # Analyze clustering results
        cluster_analysis = {}
        for i in range(n_clusters):
            cluster_robots = self.df.iloc[[j for j, c in enumerate(clusters) if c == i]]
            
            cluster_analysis[f'cluster_{i}'] = {
                'size': len(cluster_robots),
                'dominant_class': cluster_robots['class'].mode().iloc[0] if len(cluster_robots['class'].mode()) > 0 else 'Unknown',
                'dominant_region': cluster_robots['region_name'].mode().iloc[0] if len(cluster_robots['region_name'].mode()) > 0 else 'Unknown',
                'avg_year': cluster_robots[cluster_robots['year'] > 0]['year'].mean() if len(cluster_robots[cluster_robots['year'] > 0]) > 0 else 2000,
                'robots': cluster_robots[['id', 'name', 'class', 'region_name', 'year']].to_dict('records')
            }
        
        return {
            'clusters': cluster_analysis,
            'pca_components': pca.components_,
            'explained_variance': pca.explained_variance_ratio_,
            'cluster_centers': kmeans.cluster_centers_,
            'feature_matrix_pca': feature_matrix_pca,
            'cluster_labels': clusters
        }

    def generate_insights(self):
        """生成洞察报告"""
        insights = {}
        
        # 基本统计
        insights['basic_stats'] = {
            'total_robots': len(self.df),
            'total_regions': len(self.df['region_name'].unique()),
            'total_classes': len(self.df['class'].unique()),
            'total_sectors': len(self.df['sector'].unique()),
            'year_range': [
                int(self.df[self.df['year'] > 0]['year'].min()),
                int(self.df[self.df['year'] > 0]['year'].max())
            ] if len(self.df[self.df['year'] > 0]) > 0 else [2000, 2025]
        }
        
        # 趋势分析
        temporal_trends = self.analyze_temporal_trends()
        insights['trends'] = {
            'peak_year': int(temporal_trends['count'].idxmax()),
            'peak_count': int(temporal_trends['count'].max()),
            'recent_growth': float(temporal_trends['growth_rate'].tail(5).mean()) if len(temporal_trends) > 5 else 0,
            'total_growth': float((temporal_trends['count'].iloc[-1] / temporal_trends['count'].iloc[0] - 1) * 100) if len(temporal_trends) > 1 else 0
        }
        
        # 地区分析
        regional_patterns = self.analyze_regional_patterns()
        top_regions = regional_patterns['stats']['count'].sort_values(ascending=False).head(5)
        insights['regional'] = {
            'top_regions': {region: int(count) for region, count in top_regions.items()},
            'most_diverse_region': max(regional_patterns['specialization'].keys(), 
                                     key=lambda x: regional_patterns['specialization'][x]['class_diversity']),
            'most_specialized_region': min(regional_patterns['specialization'].keys(), 
                                         key=lambda x: regional_patterns['specialization'][x]['class_diversity'])
        }
        
        # 分类分析
        class_distribution = self.df['class'].value_counts()
        insights['classification'] = {
            'dominant_class': class_distribution.index[0],
            'dominant_class_count': int(class_distribution.iloc[0]),
            'class_diversity': len(class_distribution),
            'rare_classes': list(class_distribution[class_distribution == 1].index)
        }
        
        return insights

    def create_advanced_visualizations(self, output_dir="outputs/figures/"):
        """Create advanced visualizations and save as PNG images"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        visualizations = {}
        
        try:
            # 1. Temporal heatmap
            valid_data = self.df[self.df['year'] > 0]
            heatmap_data = valid_data.groupby(['year', 'class']).size().reset_index(name='count')
            heatmap_pivot = heatmap_data.pivot(index='class', columns='year', values='count').fillna(0)
            
            fig_heatmap = px.imshow(
                heatmap_pivot.values,
                x=heatmap_pivot.columns,
                y=heatmap_pivot.index,
                aspect='auto',
                title='Robot Class-Year Temporal Heatmap',
                labels={'x': 'Year', 'y': 'Robot Class', 'color': 'Count'}
            )
            fig_heatmap.update_layout(
                font=dict(size=14),
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            fig_heatmap.write_image(f"{output_dir}12_temporal_heatmap.png", 
                                  width=1600, height=1200, scale=2, engine="kaleido")
            visualizations['temporal_heatmap'] = f"{output_dir}12_temporal_heatmap.png"
            print("✅ Temporal heatmap saved")
            
            # 2. Clustering visualization
            cluster_results = self.perform_clustering_analysis()
            
            # Create PCA scatter plot
            pca_df = pd.DataFrame(
                cluster_results['feature_matrix_pca'][:, :2],
                columns=['PC1', 'PC2']
            )
            pca_df['cluster'] = cluster_results['cluster_labels']
            pca_df['class'] = self.df['class'].values
            pca_df['region'] = self.df['region_name'].values
            pca_df['name'] = self.df['name'].values
            
            fig_pca = px.scatter(
                pca_df, x='PC1', y='PC2', color='cluster',
                hover_data=['class', 'region', 'name'],
                title='Robot Clustering Analysis (PCA Visualization)',
                labels={'cluster': 'Cluster'}
            )
            fig_pca.update_layout(
                font=dict(size=14),
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            fig_pca.write_image(f"{output_dir}13_pca_clusters.png", 
                              width=1600, height=1200, scale=2, engine="kaleido")
            visualizations['pca_clusters'] = f"{output_dir}13_pca_clusters.png"
            print("✅ PCA clustering visualization saved")
            
            # 3. 3D scatter plot
            if cluster_results['feature_matrix_pca'].shape[1] >= 3:
                pca_3d_df = pd.DataFrame(
                    cluster_results['feature_matrix_pca'][:, :3],
                    columns=['PC1', 'PC2', 'PC3']
                )
                pca_3d_df['class'] = self.df['class'].values
                pca_3d_df['year'] = self.df['year'].fillna(2000).values
                pca_3d_df['name'] = self.df['name'].values
                
                fig_3d = px.scatter_3d(
                    pca_3d_df, x='PC1', y='PC2', z='PC3',
                    color='class', size='year',
                    hover_data=['name'],
                    title='Robot 3D Feature Space Distribution'
                )
                fig_3d.update_layout(
                    font=dict(size=14),
                    paper_bgcolor='white',
                    plot_bgcolor='white'
                )
                fig_3d.write_image(f"{output_dir}14_3d_scatter.png", 
                                 width=1600, height=1200, scale=2, engine="kaleido")
                visualizations['3d_scatter'] = f"{output_dir}14_3d_scatter.png"
                print("✅ 3D scatter plot saved")
            
            # 4. Sankey diagram alternative - stacked bar chart
            sankey_data = self.df[['domain', 'class', 'sector']].value_counts().reset_index(name='count')
            top_data = sankey_data.head(20)  # Top 20 combinations
            
            fig_sankey = px.bar(
                top_data, x='count', y='domain', color='class',
                title='Robot Domain-Class Distribution (Top 20 Combinations)',
                labels={'count': 'Number of Robots', 'domain': 'Domain'}
            )
            fig_sankey.update_layout(
                font=dict(size=14),
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            fig_sankey.write_image(f"{output_dir}15_domain_class_distribution.png", 
                                 width=1600, height=1000, scale=2, engine="kaleido")
            visualizations['sankey_alternative'] = f"{output_dir}15_domain_class_distribution.png"
            print("✅ Domain-class distribution saved")
            
        except Exception as e:
            print(f"Error creating advanced visualizations with Plotly: {e}")
            print("Attempting fallback to Matplotlib...")
            self._create_advanced_matplotlib_fallbacks(output_dir)
            visualizations = {
                'temporal_heatmap': f"{output_dir}12_temporal_heatmap.png",
                'pca_clusters': f"{output_dir}13_pca_clusters.png",
                'domain_class_distribution': f"{output_dir}15_domain_class_distribution.png"
            }
        
        return visualizations

    def _create_advanced_matplotlib_fallbacks(self, output_dir):
        """Create matplotlib fallback visualizations for advanced analysis"""
        import matplotlib.pyplot as plt
        
        try:
            # 1. Temporal heatmap
            valid_data = self.df[self.df['year'] > 0]
            heatmap_data = valid_data.groupby(['year', 'class']).size().reset_index(name='count')
            heatmap_pivot = heatmap_data.pivot(index='class', columns='year', values='count').fillna(0)
            
            plt.figure(figsize=(16, 10))
            plt.imshow(heatmap_pivot.values, cmap='viridis', aspect='auto')
            plt.colorbar(label='Count')
            plt.title('Robot Class-Year Temporal Heatmap', fontsize=20, fontweight='bold', pad=20)
            plt.xlabel('Year', fontsize=14)
            plt.ylabel('Robot Class', fontsize=14)
            
            # Set ticks
            plt.xticks(range(len(heatmap_pivot.columns)), heatmap_pivot.columns, rotation=45)
            plt.yticks(range(len(heatmap_pivot.index)), heatmap_pivot.index)
            plt.tight_layout()
            plt.savefig(f"{output_dir}12_temporal_heatmap.png", dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            plt.close()
            print("✅ Temporal heatmap fallback saved")
            
            # 2. PCA clustering visualization
            cluster_results = self.perform_clustering_analysis()
            pca_data = cluster_results['feature_matrix_pca'][:, :2]
            clusters = cluster_results['cluster_labels']
            
            plt.figure(figsize=(16, 12))
            scatter = plt.scatter(pca_data[:, 0], pca_data[:, 1], c=clusters, 
                                cmap='tab10', alpha=0.7, s=60)
            plt.colorbar(scatter, label='Cluster')
            plt.title('Robot Clustering Analysis (PCA Visualization)', 
                     fontsize=20, fontweight='bold', pad=20)
            plt.xlabel('First Principal Component', fontsize=14)
            plt.ylabel('Second Principal Component', fontsize=14)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(f"{output_dir}13_pca_clusters.png", dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            plt.close()
            print("✅ PCA clustering fallback saved")
            
            # 3. Domain-class distribution
            domain_class_data = self.df.groupby(['domain', 'class']).size().reset_index(name='count')
            top_data = domain_class_data.nlargest(15, 'count')
            
            plt.figure(figsize=(16, 10))
            bars = plt.barh(range(len(top_data)), top_data['count'])
            plt.title('Robot Domain-Class Distribution (Top 15)', 
                     fontsize=20, fontweight='bold', pad=20)
            plt.xlabel('Number of Robots', fontsize=14)
            plt.ylabel('Domain-Class Combinations', fontsize=14)
            
            # Create labels
            labels = [f"{row['domain']} - {row['class']}" for _, row in top_data.iterrows()]
            plt.yticks(range(len(top_data)), labels)
            
            # Color bars
            colors = plt.cm.viridis(np.linspace(0, 1, len(bars)))
            for bar, color in zip(bars, colors):
                bar.set_color(color)
            
            plt.tight_layout()
            plt.savefig(f"{output_dir}15_domain_class_distribution.png", dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            plt.close()
            print("✅ Domain-class distribution fallback saved")
            
        except Exception as e:
            print(f"Error in advanced matplotlib fallback: {e}")

    def export_processed_data(self, output_path="processed_data/"):
        """导出处理后的数据"""
        import os
        os.makedirs(output_path, exist_ok=True)
        
        # 导出主数据框
        self.df.to_csv(f"{output_path}processed_robots.csv", index=False, encoding='utf-8')
        
        # 导出分析结果
        insights = self.generate_insights()
        with open(f"{output_path}insights.json", 'w', encoding='utf-8') as f:
            json.dump(insights, f, ensure_ascii=False, indent=2)
        
        # 导出时间趋势
        temporal_trends = self.analyze_temporal_trends()
        temporal_trends.to_csv(f"{output_path}temporal_trends.csv", encoding='utf-8')
        
        # 导出地区分析
        regional_patterns = self.analyze_regional_patterns()
        regional_patterns['stats'].to_csv(f"{output_path}regional_stats.csv", encoding='utf-8')
        
        with open(f"{output_path}regional_specialization.json", 'w', encoding='utf-8') as f:
            json.dump(regional_patterns['specialization'], f, ensure_ascii=False, indent=2)
        
        # 导出聚类结果
        cluster_results = self.perform_clustering_analysis()
        with open(f"{output_path}cluster_analysis.json", 'w', encoding='utf-8') as f:
            # 移除不能序列化的numpy数组
            exportable_results = {
                'clusters': cluster_results['clusters'],
                'explained_variance': cluster_results['explained_variance'].tolist()
            }
            json.dump(exportable_results, f, ensure_ascii=False, indent=2)
        
        print(f"处理后的数据已导出到 {output_path}")
        
        return {
            'processed_dataframe': f"{output_path}processed_robots.csv",
            'insights': f"{output_path}insights.json",
            'temporal_trends': f"{output_path}temporal_trends.csv",
            'regional_stats': f"{output_path}regional_stats.csv",
            'cluster_analysis': f"{output_path}cluster_analysis.json"
        }


def main():
    """主函数"""
    print("初始化数据处理器...")
    processor = RobotDataProcessor()
    
    print("生成洞察报告...")
    insights = processor.generate_insights()
    print("\n=== 数据洞察报告 ===")
    print(f"机器人总数: {insights['basic_stats']['total_robots']}")
    print(f"涉及地区: {insights['basic_stats']['total_regions']}")
    print(f"机器人类别: {insights['basic_stats']['total_classes']}")
    print(f"年份范围: {insights['basic_stats']['year_range'][0]}-{insights['basic_stats']['year_range'][1]}")
    print(f"主导类别: {insights['classification']['dominant_class']} ({insights['classification']['dominant_class_count']}个)")
    print(f"前五地区: {list(insights['regional']['top_regions'].keys())}")
    
    print("\n创建高级可视化...")
    visualizations = processor.create_advanced_visualizations()
    print(f"生成了 {len(visualizations)} 个可视化图表")
    
    print("\n导出处理后的数据...")
    exported_files = processor.export_processed_data()
    print("导出完成!")
    
    return processor, insights, visualizations


if __name__ == "__main__":
    main()
