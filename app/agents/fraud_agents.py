"""
Fraud Detection Agents using CrewAI
"""

from crewai import Agent, Task, Crew
from app.config.settings import settings
import json


class FraudDetectionAgents:
    """Collection of AI agents for fraud detection"""
    
    def __init__(self):
        self.agents = self._create_agents()
        self.crew = self._create_crew()
    
    def _create_agents(self):
        """Create specialized fraud detection agents"""
        
        # Amount Analysis Agent
        amount_agent = Agent(
            role="Amount Analysis Specialist",
            goal="Analyze transaction amounts for unusual patterns",
            backstory="You are an expert in detecting unusual spending patterns and amount-based fraud indicators.",
            verbose=True,
            allow_delegation=False
        )
        
        # Behavioral Analysis Agent
        behavior_agent = Agent(
            role="Behavioral Analysis Specialist",
            goal="Analyze user behavior patterns for anomalies",
            backstory="You specialize in understanding normal vs abnormal user transaction behaviors.",
            verbose=True,
            allow_delegation=False
        )
        
        # Location Analysis Agent
        location_agent = Agent(
            role="Location Analysis Specialist",
            goal="Analyze transaction locations for suspicious activities",
            backstory="You are an expert in geographic fraud patterns and location-based risk assessment.",
            verbose=True,
            allow_delegation=False
        )
        
        # Risk Assessment Agent
        risk_agent = Agent(
            role="Risk Assessment Coordinator",
            goal="Coordinate all analysis and make final fraud determination",
            backstory="You are the final decision maker who weighs all evidence from other agents.",
            verbose=True,
            allow_delegation=False
        )
        
        return {
            'amount': amount_agent,
            'behavior': behavior_agent,
            'location': location_agent,
            'risk': risk_agent
        }
    
    def _create_crew(self):
        """Create the crew of agents"""
        return Crew(
            agents=list(self.agents.values()),
            verbose=True
        )
    
    def analyze_transaction(self, transaction_data):
        """Analyze a transaction using all agents"""
        
        # Create tasks for each agent
        tasks = []
        
        # Amount analysis task
        amount_task = Task(
            description=f"""
            Analyze the transaction amount: ${transaction_data['amount']}
            Transaction type: {transaction_data['transaction_type']}
            User ID: {transaction_data['user_id']}
            
            Look for:
            - Unusually high amounts
            - Round number patterns
            - Amounts that don't match typical patterns
            
            Return your analysis as: SUSPICIOUS or NORMAL with reasoning.
            """,
            agent=self.agents['amount']
        )
        
        # Behavior analysis task
        behavior_task = Task(
            description=f"""
            Analyze the transaction behavior:
            User ID: {transaction_data['user_id']}
            Transaction type: {transaction_data['transaction_type']}
            Time: {transaction_data['timestamp']}
            
            Look for:
            - Unusual transaction timing
            - Frequency patterns
            - Transaction type patterns
            
            Return your analysis as: SUSPICIOUS or NORMAL with reasoning.
            """,
            agent=self.agents['behavior']
        )
        
        # Location analysis task
        location_task = Task(
            description=f"""
            Analyze the transaction location:
            Location: {transaction_data.get('location', 'Unknown')}
            Merchant: {transaction_data.get('merchant', 'Unknown')}
            User ID: {transaction_data['user_id']}
            
            Look for:
            - Unusual locations
            - High-risk merchants
            - Geographic inconsistencies
            
            Return your analysis as: SUSPICIOUS or NORMAL with reasoning.
            """,
            agent=self.agents['location']
        )
        
        # Risk assessment task
        risk_task = Task(
            description=f"""
            Based on all previous analyses, make a final fraud determination.
            
            Consider:
            - Amount analysis results
            - Behavior analysis results
            - Location analysis results
            
            Provide final verdict: FRAUD or LEGITIMATE
            Include confidence score (0-1)
            List key risk factors
            """,
            agent=self.agents['risk']
        )
        
        tasks = [amount_task, behavior_task, location_task, risk_task]
        
        # Execute the crew
        result = self.crew.kickoff(tasks=tasks)
        
        return self._process_results(result)
    
    def _process_results(self, crew_result):
        """Process crew results into structured format"""
        # Simple processing - in a real implementation, this would be more sophisticated
        result_text = str(crew_result)
        
        # Basic fraud detection logic based on agent responses
        is_fraud = "FRAUD" in result_text.upper()
        confidence = 0.8 if is_fraud else 0.2
        
        # Extract risk factors (simplified)
        risk_factors = []
        if "suspicious" in result_text.lower():
            risk_factors.append("Suspicious patterns detected")
        if "unusual" in result_text.lower():
            risk_factors.append("Unusual behavior")
        
        # Agent votes (simplified)
        agent_votes = {
            "amount_agent": "SUSPICIOUS" in result_text,
            "behavior_agent": "SUSPICIOUS" in result_text,
            "location_agent": "SUSPICIOUS" in result_text,
            "risk_agent": is_fraud
        }
        
        return {
            "is_fraud": is_fraud,
            "confidence_score": confidence,
            "risk_factors": risk_factors,
            "agent_votes": agent_votes,
            "raw_analysis": result_text
        } 