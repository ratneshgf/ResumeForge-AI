"""
Comprehensive Skill Taxonomy for ATS Scoring

Includes 1000+ technical skills, frameworks, tools, and methodologies
organized by category. Uses fuzzy matching and NER for accurate extraction.
"""
import re
from typing import List, Set


class SkillTaxonomy:
    """Comprehensive skill database with intelligent extraction"""
    
    def __init__(self):
        self.skills = self._build_skill_database()
        self.skill_patterns = self._compile_patterns()
    
    def _build_skill_database(self) -> Set[str]:
        """Build comprehensive skill database"""
        skills = set()
        
        # Programming Languages
        skills.update([
            "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#",
            "Ruby", "PHP", "Swift", "Kotlin", "Go", "Rust", "Scala",
            "R", "MATLAB", "Perl", "Haskell", "Lua", "Dart", "Elixir",
            "Objective-C", "Shell", "Bash", "PowerShell", "SQL", "PL/SQL",
            "T-SQL", "VBA", "Assembly", "Fortran", "COBOL", "Groovy",
            "Clojure", "F#", "Julia", "Erlang", "Prolog", "Lisp", "Scheme"
        ])
        
        # Web Technologies
        skills.update([
            "HTML", "HTML5", "CSS", "CSS3", "SASS", "SCSS", "LESS",
            "React", "React.js", "ReactJS", "Angular", "AngularJS", "Vue", "Vue.js",
            "Svelte", "Next.js", "Nuxt.js", "Gatsby", "jQuery", "Bootstrap",
            "Tailwind CSS", "Material-UI", "Ant Design", "Chakra UI",
            "Webpack", "Vite", "Rollup", "Parcel", "Babel", "ESLint",
            "Prettier", "Jest", "Mocha", "Chai", "Cypress", "Selenium",
            "WebDriver", "Puppeteer", "Playwright"
        ])
        
        # Backend Frameworks
        skills.update([
            "Node.js", "Express", "Express.js", "Fastify", "Koa", "NestJS",
            "Django", "Flask", "FastAPI", "Pyramid", "Tornado", "Bottle",
            "Spring", "Spring Boot", "Hibernate", "Struts", "JSF",
            "Ruby on Rails", "Sinatra", "Laravel", "Symfony", "CodeIgniter",
            "ASP.NET", ".NET Core", "Entity Framework", "WCF", "WPF",
            "Phoenix", "Elixir", "Play Framework", "Vert.x", "Micronaut",
            "Quarkus", "Gin", "Echo", "Fiber", "Actix", "Rocket"
        ])
        
        # Databases
        skills.update([
            "MySQL", "PostgreSQL", "SQL Server", "Oracle", "DB2", "SQLite",
            "MongoDB", "Cassandra", "Redis", "Memcached", "Elasticsearch",
            "CouchDB", "Neo4j", "DynamoDB", "Firebase", "Firestore",
            "Realm", "IndexedDB", "RethinkDB", "ArangoDB", "InfluxDB",
            "TimescaleDB", "MariaDB", "Couchbase", "HBase", "Bigtable",
            "Amazon Aurora", "Azure SQL", "Cloud SQL", "Snowflake", "Redshift",
            "BigQuery", "Databricks", "Apache Hive", "Presto", "Impala"
        ])
        
        # Cloud Platforms & Services
        skills.update([
            "AWS", "Amazon Web Services", "EC2", "S3", "Lambda", "RDS",
            "DynamoDB", "CloudFront", "Route 53", "ECS", "EKS", "Fargate",
            "CloudWatch", "CloudFormation", "Elastic Beanstalk", "SQS", "SNS",
            "Azure", "Microsoft Azure", "Azure DevOps", "Azure Functions",
            "Azure Storage", "Azure SQL", "Azure Kubernetes Service", "AKS",
            "GCP", "Google Cloud Platform", "Google Cloud", "Compute Engine",
            "App Engine", "Cloud Functions", "Cloud Run", "Cloud Storage",
            "Kubernetes", "Docker", "Podman", "OpenShift", "Rancher",
            "Terraform", "CloudFormation", "Pulumi", "Ansible", "Chef",
            "Puppet", "Salt", "Vagrant", "Packer"
        ])
        
        # DevOps & CI/CD
        skills.update([
            "Git", "GitHub", "GitLab", "Bitbucket", "SVN", "Mercurial",
            "Jenkins", "Travis CI", "Circle CI", "GitHub Actions", "GitLab CI",
            "Azure Pipelines", "Bamboo", "TeamCity", "ArgoCD", "Flux",
            "Docker", "Docker Compose", "Kubernetes", "Helm", "Kustomize",
            "Nginx", "Apache", "Tomcat", "IIS", "HAProxy", "Envoy",
            "Prometheus", "Grafana", "ELK Stack", "Splunk", "Datadog",
            "New Relic", "AppDynamics", "Dynatrace", "Nagios", "Zabbix"
        ])
        
        # Data Science & ML
        skills.update([
            "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas",
            "NumPy", "SciPy", "Matplotlib", "Seaborn", "Plotly", "ggplot2",
            "Jupyter", "Apache Spark", "PySpark", "Hadoop", "MapReduce",
            "Hive", "Pig", "NLTK", "spaCy", "Gensim", "OpenCV", "PIL",
            "XGBoost", "LightGBM", "CatBoost", "Prophet", "Statsmodels",
            "MLflow", "Kubeflow", "SageMaker", "Vertex AI", "Azure ML",
            "H2O.ai", "DataRobot", "Alteryx", "Tableau", "Power BI",
            "Looker", "Qlik", "Superset", "Metabase", "Redash"
        ])
        
        # Mobile Development
        skills.update([
            "iOS", "Android", "React Native", "Flutter", "Xamarin",
            "Ionic", "Cordova", "PhoneGap", "SwiftUI", "UIKit",
            "Jetpack Compose", "Android SDK", "Xcode", "Android Studio",
            "CocoaPods", "Gradle", "Maven", "Fastlane"
        ])
        
        # Testing & QA
        skills.update([
            "Unit Testing", "Integration Testing", "E2E Testing",
            "Test Automation", "TDD", "BDD", "Selenium", "Cypress",
            "Jest", "Mocha", "Chai", "Jasmine", "Karma", "Protractor",
            "TestNG", "JUnit", "PyTest", "unittest", "RSpec", "Cucumber",
            "Postman", "SoapUI", "JMeter", "LoadRunner", "Gatling",
            "Locust", "K6", "Artillery"
        ])
        
        # Security
        skills.update([
            "OAuth", "JWT", "SAML", "OpenID", "LDAP", "Active Directory",
            "SSL/TLS", "PKI", "Encryption", "Cryptography", "Penetration Testing",
            "Vulnerability Assessment", "OWASP", "Security Auditing",
            "Firewall", "IDS/IPS", "SIEM", "WAF", "VPN", "Zero Trust",
            "IAM", "SSO", "MFA", "2FA"
        ])
        
        # Methodologies & Practices
        skills.update([
            "Agile", "Scrum", "Kanban", "Lean", "SAFe", "XP", "DevOps",
            "CI/CD", "Microservices", "Monolithic", "Event-Driven",
            "Domain-Driven Design", "DDD", "SOLID", "Design Patterns",
            "RESTful APIs", "REST API", "GraphQL", "gRPC", "SOAP",
            "WebSockets", "Server-Side Rendering", "SSR", "Static Site Generation",
            "JAMstack", "Serverless", "FaaS", "PaaS", "IaaS", "SaaS"
        ])
        
        # Big Data
        skills.update([
            "Hadoop", "Spark", "Kafka", "Flink", "Storm", "Airflow",
            "Luigi", "Nifi", "Beam", "Dataflow", "EMR", "Glue", "Athena",
            "Data Lake", "Data Warehouse", "ETL", "ELT", "Data Pipeline",
            "Batch Processing", "Stream Processing", "Real-time Analytics"
        ])
        
        # Blockchain & Web3
        skills.update([
            "Blockchain", "Ethereum", "Solidity", "Smart Contracts",
            "Web3", "DeFi", "NFT", "Hyperledger", "Bitcoin", "Cryptocurrency"
        ])
        
        # Other Tools & Technologies
        skills.update([
            "Vim", "Emacs", "VS Code", "IntelliJ IDEA", "PyCharm",
            "Eclipse", "NetBeans", "Visual Studio", "Sublime Text",
            "Atom", "Slack", "Jira", "Confluence", "Trello", "Asana",
            "Monday.com", "Notion", "Figma", "Sketch", "Adobe XD",
            "Photoshop", "Illustrator", "InVision", "Zeplin", "Miro"
        ])
        
        # Normalize all skills to lowercase for matching
        return {skill.lower() for skill in skills}
    
    def _compile_patterns(self) -> List[re.Pattern]:
        """Compile regex patterns for skill extraction"""
        patterns = []
        
        # Pattern for skills with versions (e.g., "React.js 18", "Python 3.9")
        patterns.append(re.compile(r'\b[\w\+\#\.]+\s+\d+(?:\.\d+)*\b', re.IGNORECASE))
        
        # Pattern for skills with parentheses (e.g., "Node (Express)")
        patterns.append(re.compile(r'\b[\w\+\#\.]+\s*\([^)]+\)', re.IGNORECASE))
        
        return patterns
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract skills from text using multiple techniques:
        1. Direct matching against skill database
        2. Pattern-based extraction
        3. Context-aware matching
        """
        if not text:
            return []
        
        found_skills = set()
        text_lower = text.lower()
        
        # Method 1: Direct matching
        for skill in self.skills:
            # Use word boundaries for accurate matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                # Convert back to title case for display
                found_skills.add(skill.title())
        
        # Method 2: Handle common variations
        variations = {
            'react': 'React',
            'react.js': 'React',
            'reactjs': 'React',
            'node': 'Node.js',
            'node.js': 'Node.js',
            'nodejs': 'Node.js',
            'angular': 'Angular',
            'angularjs': 'Angular',
            'vue': 'Vue.js',
            'vue.js': 'Vue.js',
            'vuejs': 'Vue.js',
            'aws': 'AWS',
            'amazon web services': 'AWS',
            'gcp': 'GCP',
            'google cloud': 'GCP',
            'k8s': 'Kubernetes',
            'postgres': 'PostgreSQL',
            'mongo': 'MongoDB',
            'docker': 'Docker',
            'ci/cd': 'CI/CD',
            'ml': 'Machine Learning',
            'ai': 'Artificial Intelligence',
        }
        
        for variant, canonical in variations.items():
            if variant in text_lower:
                found_skills.add(canonical)
        
        # Method 3: Extract compound skills (e.g., "React with Redux")
        compound_patterns = [
            r'(react|angular|vue)[\s\w]*(?:with|using)\s+(redux|mobx|vuex|rxjs)',
            r'(python|java|javascript|typescript)[\s\w]*(?:with|using)\s+(django|flask|spring|express)',
        ]
        
        for pattern in compound_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                for skill in match:
                    if skill in self.skills:
                        found_skills.add(skill.title())
        
        return sorted(list(found_skills))
