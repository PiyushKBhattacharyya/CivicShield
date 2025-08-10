import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
import json
import logging
from typing import Dict, Any, List
import uuid

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreatDetector:
    def __init__(self):
        """
        Initialize the threat detection system with pre-trained models
        """
        # Initialize text processing models
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.bert_model = AutoModel.from_pretrained("bert-base-uncased")
        
        # Initialize anomaly detection models
        self.isolation_forest = IsolationForest(contamination=0.1)
        self.scaler = StandardScaler()
        
        # Initialize text classification vectorizer
        self.tfidf = TfidfVectorizer(max_features=1000, stop_words='english')
        
        # Initialize clustering for pattern detection
        self.kmeans = KMeans(n_clusters=5)
        
        logger.info("Threat detection models initialized")
    
    def process_text(self, text: str) -> np.ndarray:
        """
        Process text using BERT embeddings
        """
        try:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            with torch.no_grad():
                outputs = self.bert_model(**inputs)
            # Use the CLS token embedding as the text representation
            embeddings = outputs.last_hidden_state[:, 0, :].numpy()
            return embeddings.flatten()
        except Exception as e:
            logger.error(f"Error processing text: {str(e)}")
            return np.zeros(768)  # BERT base has 768 dimensions
    
    def detect_anomalies(self, sensor_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect anomalies in sensor data
        """
        try:
            # Convert to DataFrame
            df = pd.DataFrame(sensor_data)
            
            # Extract numerical features
            numerical_cols = df.select_dtypes(include=[np.number]).columns
            if len(numerical_cols) == 0:
                return []
            
            # Scale the data
            scaled_data = self.scaler.fit_transform(df[numerical_cols])
            
            # Fit isolation forest
            self.isolation_forest.fit(scaled_data)
            
            # Predict anomalies
            predictions = self.isolation_forest.predict(scaled_data)
            anomaly_scores = self.isolation_forest.decision_function(scaled_data)
            
            # Create results
            anomalies = []
            for i, (prediction, score) in enumerate(zip(predictions, anomaly_scores)):
                if prediction == -1:  # Anomaly detected
                    anomalies.append({
                        "data_id": str(uuid.uuid4()),
                        "timestamp": df.iloc[i].get("timestamp", None),
                        "anomaly_score": float(score),
                        "severity": "high" if score < -0.5 else "medium",
                        "features": df.iloc[i].to_dict()
                    })
            
            return anomalies
        except Exception as e:
            logger.error(f"Error detecting anomalies: {str(e)}")
            return []
    
    def analyze_social_media(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze social media posts for threat indicators
        """
        try:
            # Extract text content
            texts = [post.get("content", "") for post in posts]
            if not texts:
                return []
            
            # Process texts with BERT
            embeddings = np.array([self.process_text(text) for text in texts])
            
            # Cluster similar posts
            if len(embeddings) > 5:  # Only cluster if we have enough data
                clusters = self.kmeans.fit_predict(embeddings)
            else:
                clusters = [0] * len(embeddings)
            
            # Analyze sentiment (simplified)
            threat_keywords = ["attack", "bomb", "threat", "danger", "emergency", "violence"]
            threat_scores = []
            
            for text in texts:
                score = sum(1 for keyword in threat_keywords if keyword in text.lower())
                threat_scores.append(score)
            
            # Create results
            results = []
            for i, (post, cluster, score) in enumerate(zip(posts, clusters, threat_scores)):
                if score > 0:  # Potential threat detected
                    results.append({
                        "post_id": post.get("post_id", str(uuid.uuid4())),
                        "platform": post.get("platform", "unknown"),
                        "content": post.get("content", ""),
                        "threat_score": score,
                        "cluster": int(cluster),
                        "timestamp": post.get("timestamp", None),
                        "location": post.get("location", None),
                        "severity": "high" if score > 2 else "medium"
                    })
            
            return results
        except Exception as e:
            logger.error(f"Error analyzing social media: {str(e)}")
            return []
    
    def detect_patterns(self, threat_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect patterns in threat data
        """
        try:
            # Extract text descriptions
            texts = [data.get("description", "") + " " + data.get("title", "") for data in threat_data]
            if not texts:
                return []
            
            # Vectorize texts
            tfidf_matrix = self.tfidf.fit_transform(texts)
            
            # Cluster similar threats
            clusters = self.kmeans.fit_predict(tfidf_matrix.toarray())
            
            # Identify common patterns
            patterns = []
            for cluster_id in range(self.kmeans.n_clusters):
                cluster_indices = np.where(clusters == cluster_id)[0]
                if len(cluster_indices) > 1:  # Only consider clusters with multiple items
                    # Get common terms for this cluster
                    cluster_texts = [texts[i] for i in cluster_indices]
                    cluster_tfidf = self.tfidf.transform(cluster_texts)
                    feature_names = self.tfidf.get_feature_names_out()
                    
                    # Get top terms for this cluster
                    mean_tfidf = cluster_tfidf.mean(axis=0).A1
                    top_terms_idx = mean_tfidf.argsort()[-5:][::-1]
                    top_terms = [feature_names[idx] for idx in top_terms_idx if mean_tfidf[idx] > 0]
                    
                    patterns.append({
                        "pattern_id": str(uuid.uuid4()),
                        "cluster_id": int(cluster_id),
                        "count": len(cluster_indices),
                        "common_terms": top_terms,
                        "severity": "high" if len(cluster_indices) > 5 else "medium"
                    })
            
            return patterns
        except Exception as e:
            logger.error(f"Error detecting patterns: {str(e)}")
            return []
    
    def generate_threat_report(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive threat report
        """
        try:
            report = {
                "report_id": str(uuid.uuid4()),
                "generated_at": pd.Timestamp.now().isoformat(),
                "summary": {
                    "total_threats": len(analysis_results.get("threats", [])),
                    "high_severity_count": len([t for t in analysis_results.get("threats", []) if t.get("severity") == "high"]),
                    "anomalies_detected": len(analysis_results.get("anomalies", [])),
                    "social_threats": len(analysis_results.get("social_media_threats", [])),
                    "patterns_identified": len(analysis_results.get("patterns", []))
                },
                "threats": analysis_results.get("threats", []),
                "anomalies": analysis_results.get("anomalies", []),
                "social_media_threats": analysis_results.get("social_media_threats", []),
                "patterns": analysis_results.get("patterns", []),
                "recommendations": self._generate_recommendations(analysis_results)
            }
            
            return report
        except Exception as e:
            logger.error(f"Error generating threat report: {str(e)}")
            return {"error": str(e)}
    
    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on analysis results
        """
        recommendations = []
        
        # Check for high severity threats
        high_threats = [t for t in analysis_results.get("threats", []) if t.get("severity") == "high"]
        if len(high_threats) > 0:
            recommendations.append(f"Investigate {len(high_threats)} high severity threats immediately")
        
        # Check for anomalies
        anomalies = analysis_results.get("anomalies", [])
        if len(anomalies) > 5:
            recommendations.append(f"Review {len(anomalies)} detected anomalies for potential security issues")
        
        # Check for social media threats
        social_threats = analysis_results.get("social_media_threats", [])
        if len(social_threats) > 10:
            recommendations.append(f"Monitor social media activity closely - {len(social_threats)} potential threats detected")
        
        # Check for patterns
        patterns = analysis_results.get("patterns", [])
        if len(patterns) > 0:
            recommendations.append(f"Investigate {len(patterns)} identified threat patterns for coordinated activities")
        
        # General recommendation
        if len(recommendations) == 0:
            recommendations.append("Continue monitoring for potential threats")
        
        return recommendations

# Example usage
if __name__ == "__main__":
    # Initialize threat detector
    detector = ThreatDetector()
    
    # Example threat data
    sample_threats = [
        {
            "title": "Suspicious Network Activity",
            "description": "Unusual network traffic detected from unknown IP addresses",
            "severity": "high",
            "type": "cyber"
        },
        {
            "title": "Potential Security Breach",
            "description": "Unauthorized access attempt to secure facility",
            "severity": "high",
            "type": "physical"
        }
    ]
    
    # Example sensor data
    sample_sensor_data = [
        {"temperature": 25.5, "humidity": 60.2, "pressure": 1013.25},
        {"temperature": 26.1, "humidity": 59.8, "pressure": 1012.98},
        {"temperature": 50.0, "humidity": 30.0, "pressure": 950.0},  # Anomaly
    ]
    
    # Example social media posts
    sample_posts = [
        {
            "content": "Be careful in downtown area today, potential threat",
            "platform": "twitter",
            "timestamp": "2023-01-01T12:00:00Z"
        },
        {
            "content": "Bomb threat at city hall, stay away",
            "platform": "facebook",
            "timestamp": "2023-01-01T12:05:00Z"
        }
    ]
    
    # Process data
    anomalies = detector.detect_anomalies(sample_sensor_data)
    social_threats = detector.analyze_social_media(sample_posts)
    patterns = detector.detect_patterns(sample_threats)
    
    # Generate report
    analysis_results = {
        "threats": sample_threats,
        "anomalies": anomalies,
        "social_media_threats": social_threats,
        "patterns": patterns
    }
    
    report = detector.generate_threat_report(analysis_results)
    print(json.dumps(report, indent=2))