import json
from datetime import datetime
import os
import logging

logger = logging.getLogger('bookfinder.rag')

class RAGService:
    """Retrieval-Augmented Generation service for logging and retrieving user interactions"""
    
    LOG_FILE = "user_interactions.log"
    
    @staticmethod
    def log_interaction(user_id, query, books_found, command_type, response_text=None):
        """
        Log user interactions for future analysis and personalization
        
        Args:
            user_id (int): Discord user ID
            query (str): User's search query or preferences
            books_found (list): List of book results
            command_type (str): Type of command (findbook/recommend)
            response_text (str): AI-generated response text
        """
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_id": str(user_id),
                "query": query,
                "command": command_type,
                "books_found": len(books_found) if books_found else 0,
                "books": [
                    {
                        "title": book.get("title", "Unknown"),
                        "authors": book.get("authors", ["Unknown"]),
                        "categories": book.get("categories", [])
                    } for book in (books_found[:3] if books_found else [])
                ],
                "ai_response": response_text[:200] if response_text else None  # First 200 chars
            }
            
            # Append to log file
            with open(RAGService.LOG_FILE, "a", encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
                
            logger.info(f"Logged interaction for user {user_id}: {command_type} - {query[:50]}...")
            
        except Exception as e:
            logger.error(f"Error logging interaction: {e}")
    
    @staticmethod
    def get_user_history(user_id, limit=10):
        """
        Get user's search history
        
        Args:
            user_id (int): Discord user ID
            limit (int): Maximum number of entries to return
            
        Returns:
            list: List of user's recent interactions
        """
        if not os.path.exists(RAGService.LOG_FILE):
            return []
            
        user_interactions = []
        try:
            with open(RAGService.LOG_FILE, "r", encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        if entry["user_id"] == str(user_id):
                            user_interactions.append(entry)
                    except json.JSONDecodeError:
                        continue
                        
            # Return most recent interactions
            return user_interactions[-limit:] if user_interactions else []
            
        except Exception as e:
            logger.error(f"Error reading user history: {e}")
            return []
    
    @staticmethod
    def get_user_preferences(user_id):
        """
        Analyze user's search history to extract preferences
        
        Args:
            user_id (int): Discord user ID
            
        Returns:
            dict: User preferences analysis
        """
        history = RAGService.get_user_history(user_id, limit=20)
        
        if not history:
            return {"genres": [], "authors": [], "recent_queries": []}
        
        # Extract common genres and authors
        genres = []
        authors = []
        queries = []
        
        for interaction in history:
            queries.append(interaction.get("query", ""))
            
            for book in interaction.get("books", []):
                if book.get("categories"):
                    genres.extend(book["categories"])
                if book.get("authors"):
                    authors.extend(book["authors"])
        
        # Count occurrences and get most common
        from collections import Counter
        
        return {
            "genres": [genre for genre, count in Counter(genres).most_common(5)],
            "authors": [author for author, count in Counter(authors).most_common(5)],
            "recent_queries": queries[-5:],
            "total_interactions": len(history)
        }
    
    @staticmethod
    def get_analytics():
        """
        Get overall system analytics
        
        Returns:
            dict: System-wide usage analytics
        """
        if not os.path.exists(RAGService.LOG_FILE):
            return {"total_interactions": 0, "unique_users": 0}
        
        interactions = []
        users = set()
        commands = {"findbook": 0, "recommend": 0}
        
        try:
            with open(RAGService.LOG_FILE, "r", encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        interactions.append(entry)
                        users.add(entry["user_id"])
                        command_type = entry.get("command", "unknown")
                        if command_type in commands:
                            commands[command_type] += 1
                    except json.JSONDecodeError:
                        continue
                        
            return {
                "total_interactions": len(interactions),
                "unique_users": len(users),
                "findbook_uses": commands["findbook"],
                "recommend_uses": commands["recommend"],
                "last_activity": interactions[-1]["timestamp"] if interactions else None
            }
            
        except Exception as e:
            logger.error(f"Error getting analytics: {e}")
            return {"total_interactions": 0, "unique_users": 0} 