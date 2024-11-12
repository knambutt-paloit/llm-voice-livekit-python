from enum import Enum

# consultant_db.py
TRUE_DIGITAL_THAILAND_TRUEID = "True Digital Thailand - TrueID"

class RoleDevEnum(Enum):
    FULL_STACK_DEVELOPER = "Full Stack Developer"
    TECHNICAL_LEAD = "Technical Lead"
    DEVOPS_LEAD = "DevOps Lead"

class RoleDesignEnum(Enum):
    HEAD_OF_UX_UI_DESIGN = "Head of UX/UI Design"
    UX_UI_DESIGNER = "UX/UI Designer"

class RoleScrumEnum(Enum):
    PRODUCT_OWNER = "Product Owner"
    AGILE_DELIVERY_LEAD = "Agile Delivery Lead"
    SCRUM_MASTER = "Scrum Master"

class RoleOtherEnum(Enum):
    CHIEF_OPERATIONS_OFFICER = "Chief Operations Officer"
    SUSTANABILITY_IMPACT_LEAD = "Sustainability & Impact Lead"
    SUSTANABILITY_ASSISTANT_MANAGER = "Sustainability Assistant Manager"

# Combine all enums into a dictionary
combined_roles = {**RoleDevEnum.__members__, **RoleDesignEnum.__members__, **RoleScrumEnum.__members__, **RoleOtherEnum.__members__}

# Create a new combined enum using the functional API
Roles = Enum("Roles", combined_roles)

PALO_IT_CONSULTANTS = [
    {
        "id": "con-001",
        "department": "Technology",
        "name": "Sarin Suriyakoon",
        "role": Roles.TECHNICAL_LEAD,
        "yearsOfExperience": 10,
        "skills": ["LLM", "Solution Architect", "AI", "Typescript", "React", "Flutter", "Spring Boot"],
        "certifications": ["AWS Developer Associate", "AWS Solution Architect Associate", "CKAD"],
        "isAvailable": True,
        "projectsDone": ["Superapp", "Microsoft AI Strategy", "Google Data Science"],
    },
    {
        "id": 'uuid-1',
        "department": 'Sustainability',
        "name": 'Patchareeboon Sakulpitakphon',
        "role": Roles.SUSTANABILITY_IMPACT_LEAD,
        "yearsOfExperience": 18,
        "skills": ['Sustainability', 'Corporate Partnerships', 'ESG Advisory', 'Human Rights'],
        "certifications": ['Master of Arts in International Policy Studies'],
        "isAvailable": True,
        "projectsDone": ['UNDP Laos', 'RTI International', 'Resonance'],
    },
    {
        "id": 'uuid-2',
        "department": 'Sustainability',
        "name": 'Kanyapak Kakkanantadilok',
        "role": Roles.SUSTANABILITY_ASSISTANT_MANAGER,
        "yearsOfExperience": 4,
        "skills": ['Climate Change Advisory', 'GHG Training', 'ESG Reporting'],
        "certifications": ['ISO 14060', 'GHG Protocol'],
        "isAvailable": True,
        "projectsDone": ['EY Company Services Limited', 'ERM-Siam Thailand'],
    },
    {
        "id": 'uuid-3',
        "department": 'Agile',
        "name": 'Ryan Clemens',
        "role": Roles.CHIEF_OPERATIONS_OFFICER,
        "yearsOfExperience": 20,
        "skills": ['Organizational Culture', 'Agile Business', 'DevOps'],
        "certifications": ['Executive MBA', 'ICAgile Team Facilitation'],
        "isAvailable": False,
        "projectsDone": ['Allianz Technology Thailand', 'Agoda'],
    },
    {
        "id": 'uuid-4',
        "department": 'Agile',
        "name": 'Jinhan Chen',
        "role": Roles.PRODUCT_OWNER,
        "yearsOfExperience": 7,
        "skills": ['Product Management', 'Agile Processes', 'Software Localization'],
        "certifications": ['ICAgile Certified Professional'],
        "isAvailable": True,
        "projectsDone": ["AIA Thailand", 'Tourism Authority of Thailand'],
    },
    {
        "id": 'uuid-5',
        "department": 'Design',
        "name": 'Harit Wanapoh',
        "role": Roles.HEAD_OF_UX_UI_DESIGN,
        "yearsOfExperience": 11,
        "skills": ['UX/UI Design', 'Sustainable UX', 'Design Systems Management'],
        "certifications": ["ICA Certified Professional"],
        "isAvailable": False,
        "projectsDone": ['AIA Thailand', 'Impact Design Workshop'],
    },
    {
        "id": 'uuid-6',
        "department": 'Design',
        "name": 'Sirintra Leenutaphong',
        "role": Roles.UX_UI_DESIGNER,
        "yearsOfExperience": 4,
        "skills": ['User Research', 'Prototyping', 'Design Systems'],
        "certifications": ['JLPT N1', 'RED Academy UX Design'],
        "isAvailable": True,
        "projectsDone": ['Bank of Ayudhya - QR Modernization', 'Swoop Buddy'],
    },
    {
        "id": 'uuid-7',
        "department": 'Technology',
        "name": 'Kittipon Kanda',
        "role": Roles.TECHNICAL_LEAD,
        "yearsOfExperience": 9,
        "skills": ['DevOps', 'Automation Testing', 'Mobile Development', 'Azure', 'Kubernetes'],
        "isAvailable": True,
        "projectsDone": ['Krungsri Nimble Thailand', TRUE_DIGITAL_THAILAND_TRUEID],
    },
    {
        "id": 'uuid-8',
        "department": 'Technology',
        "name": 'Krit Nambutt',
        "role": Roles.FULL_STACK_DEVELOPER,
        "yearsOfExperience": 4,
        "skills": ['Full Stack Development', 'Chatbot Development', 'Cloud Infrastructure'],
        "certifications": ['ICBIR 2018 Certificate', 'LINE API Workshop'],
        "isAvailable": True,
        "projectsDone": ['AIA Thailand - AIA One', 'Fastship.co'],
    },
    {
        "id": 'uuid-9',
        "name": 'Thida Tun',
        "role": Roles.FULL_STACK_DEVELOPER,
        "yearsOfExperience": 5,
        "skills": ['ReactJS', 'NodeJS', 'Mobile App Development'],
        "isAvailable": False,
        "projectsDone": [TRUE_DIGITAL_THAILAND_TRUEID, 'Wisible'],
    },
    {
        "id": 'uuid-11',
        "department": 'Agile',
        "name": 'Peerachai Kaowichakorn',
        "role": Roles.AGILE_DELIVERY_LEAD,
        "yearsOfExperience": 17,
        "skills": ['Agile Coaching', 'Extreme Programming', 'Project Management'],
        "certifications": ['ICAgile - Agile Fundamental'],
        "isAvailable": False,
        "projectsDone": ['AIA Thailand - AIA ONE', 'FWD - One Modularity Project'],
    },
    {
        "id": 'uuid-12',
        "department": 'Agile',
        "name": 'Ranida Nuangjhamnong',
        "role": Roles.SCRUM_MASTER,
        "yearsOfExperience": 13,
        "skills": ['Stakeholder Management', 'Project Management', 'Data Analysis'],
        "certifications": ['Certified ScrumMaster', 'Climate Fresk Facilitator'],
        "isAvailable": True,
        "projectsDone": ['AIA Hong Kong - Minerva', 'Agoda Thailand'],
    },
    {
        "id": 'uuid-13',
        "department": 'Design',
        "name": 'Tiwarat Kulwatthanaworapong',
        "role": Roles.UX_UI_DESIGNER,
        "yearsOfExperience": 6,
        "skills": ['User Research', 'Design Systems', 'Prototyping'],
        "certifications": ['Interaction Design Foundation - Foundations of UX Design'],
        "isAvailable": True,
        "projectsDone": ['AIA Thailand', 'FOURDIGIT Thailand'],
    },
    {
        "id": 'uuid-14',
        "department": 'Technology',
        "name": 'Thanawan Techasai',
        "role": Roles.FULL_STACK_DEVELOPER,
        "yearsOfExperience": 3,
        "skills": ['GoLang', 'Python', 'ReactJS', 'Kubernetes'],
        "isAvailable": True,
        "projectsDone": [TRUE_DIGITAL_THAILAND_TRUEID, 'T.N. Incorporation'],
    },
    {
        "id": 'uuid-15',
        "department": 'DevOps',
        "name": 'Kasidis Chaowvasin',
        "role": Roles.FULL_STACK_DEVELOPER,
        "yearsOfExperience": 5,
        "skills": ['Node.js', 'ReactJS', 'TypeScript', 'Terraform'],
        "certifications": ['ICBIR 2018', 'GitHub Actions Certified'],
        "isAvailable": False,
        "projectsDone": ['AIA Hong Kong - AIA+', "True Digital Thailand - TrueID"],
    },
    {
        "id": 'uuid-16',
        "department": 'DevOps',
        "name": 'Sakarat Kaewwichian',
        "role": Roles.FULL_STACK_DEVELOPER,
        "yearsOfExperience": 9,
        "skills": ['NodeJS', 'VueJS', 'AWS', 'DevOps Automation'],
        "certifications": ['IC Agile Certified Professional','Certificate in Kubernetes Application Developer'],
        "isAvailable": True,
        "projectsDone": [TRUE_DIGITAL_THAILAND_TRUEID, 'Siam Cement Group (SCG)'],
    },
    {
        "id": 'uuid-17',
        "department": 'DevOps',
        "name": 'Kunlanit Korsamphan',
        "role": Roles.FULL_STACK_DEVELOPER,
        "yearsOfExperience": 7,
        "skills": ['ReactJS', 'GoLang', 'Flutter', 'AWS'],
        "isAvailable": False,
        "projectsDone": [TRUE_DIGITAL_THAILAND_TRUEID, 'Muang Thai Life Assurance PCL'],
    },
    {
        "id": 'uuid-18',
        "department": 'DevOps',
        "name": 'Sirirat Rungpetcharat',
        "role": Roles.DEVOPS_LEAD,
        "yearsOfExperience": 13,
        "skills": ['DevOps', 'CI/CD Automation', 'Cloud Infrastructure', 'Terraform'],
        "isAvailable": True,
        "projectsDone": ['Builk One Group', TRUE_DIGITAL_THAILAND_TRUEID],
    },
    {
        "id": 'uuid-19',
        "department": 'DevOps',
        "name": 'Kittipon Kanda',
        "role": Roles.TECHNICAL_LEAD,
        "yearsOfExperience": 9,
        "skills": ['DevOps', 'Automation Testing', 'Mobile Development'],
        "certifications": ['Certified Kubernetes Application Developer', 'ICA Certified Professional'],
        "isAvailable": True,
        "projectsDone": ['Krungsri Nimble Thailand', 'True Digital Thailand - TrueID'],
    },
    {
        "id": 'uuid-21',
        "department": 'Technology',
        "name": 'Patchara Charoenkij',
        "role": Roles.FULL_STACK_DEVELOPER,
        "yearsOfExperience": 4,
        "skills": ['ReactJS', 'Java', 'Spring Boot', 'AWS'],
        "certifications": ['Bachelor of Computer Engineering', 'ICBIR 2018 Certificate'],
        "isAvailable": True,
        "projectsDone": ['Kasikorn Bank - KCLIMATE 1.5', 'AIA Hong Kong - AIA+'],
    },
]