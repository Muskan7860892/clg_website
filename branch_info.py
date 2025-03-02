from app import db, app
from models import Branch
with app.app_context():
    branches = [
        Branch(
            branch_code="IST01",
            branch_name="Information Science & Technology",
            vision="To be a leading center of excellence in Information Science & Technology, empowering students with cutting-edge knowledge, innovation, and research to drive digital transformation and solve real-world challenges.",
            mission="1. Quality Education: Provide a comprehensive curriculum integrating data science, cybersecurity, artificial intelligence, and cloud computing. 2. Research & Innovation: Encourage research in emerging technologies, big data analytics, and intelligent systems to address industry and societal needs. 3. Industry Collaboration: Foster partnerships with tech industries to enhance practical exposure, internships, and project-based learning. 4. Ethical & Responsible Computing: Promote ethical computing practices, cybersecurity awareness, and sustainability in technology solutions. 5. Lifelong Learning & Adaptability: Prepare students for continuous learning, professional growth, and leadership in the ever-evolving IT landscape.",
            description="This branch covers programming, networking, AI, and software development..."
        ),
        Branch(
            branch_code="CSE01",
            branch_name="Computer Science & Engineering",
            vision="To be a center of excellence in Computer Science and Engineering, fostering innovation, research, and technological advancements to empower students with cutting-edge knowledge and skills for a sustainable and inclusive future.",
            mission="1. Quality Education: Provide a strong foundation in computing principles, programming, and problem-solving through a well-structured curriculum. 2.Research & Innovation: Encourage research, innovation, and entrepreneurship by integrating emerging technologies. 3.Industry Collaboration: Establish industry partnerships to bridge the gap between academia and real-world applications. 4.Ethical & Social Responsibility: Instill ethical values, teamwork, and a commitment to societal well-being through technology. 5.Lifelong Learning: Promote continuous learning and adaptability to technological advancements.",
            description="CSE focuses on software, hardware, AI, and cloud computing..."
        ),
        Branch(
            branch_code="ME01",
            branch_name="Mechanical Engineering",
            vision="To be a center of excellence in Mechanical Engineering, fostering innovation, research, and sustainable technological advancements to address global engineering challenges and contribute to industrial and societal growth.",
            mission="1. Quality Education: Provide a strong foundation in mechanical engineering principles through a well-structured curriculum and hands-on learning. 2. Research & Innovation: Promote creativity and innovation in areas like automation, robotics, thermal engineering, and manufacturing. 3. Industry Collaboration: Bridge the gap between academia and industry by fostering collaborations, internships, and skill-based training. 4. Sustainability & Ethics: Instill ethical values, sustainability practices, and responsibility in students to develop environmentally friendly engineering solutions. 5. Lifelong Learning: Encourage adaptability to emerging technologies and continuous learning for professional growth.",
            description="ME deals with design, automation, and industrial machinery..."
        ),
        Branch(
            branch_code="CE01",
            branch_name="Civil Engineering",
            vision="To be a leader in Civil Engineering education, research, and innovation, developing professionals who contribute to sustainable infrastructure, environmental conservation, and societal well-being.",
            mission="Quality Education: Provide a strong foundation in civil engineering principles through a well-structured curriculum and practical learning. 2. Research & Innovation: Encourage advancements in structural engineering, transportation, geotechnics, water resources, and environmental engineering. 3. Industry Collaboration: Strengthen ties with industries, government bodies, and research institutions for real-world applications and skill enhancement. 4. Sustainability & Ethics: Promote eco-friendly, disaster-resilient, and cost-effective infrastructure while upholding professional ethics and safety standards. 5. Lifelong Learning: Foster continuous learning, leadership, and adaptability to evolving engineering technologies and societal needs.",
            description="CE covers infrastructure design, construction, and urban planning..."
        ),
        Branch(
            branch_code="EEE01",
            branch_name="Electrical & Electronics Engineering",
            vision="To be a center of excellence in Electrical and Electronics Engineering, fostering innovation, research, and sustainable technological advancements to meet global challenges and contribute to societal development.",
            mission="1. Quality Education: Provide a strong foundation in electrical and electronics engineering principles through a well-structured curriculum and hands-on learning. 2. Innovation & Research: Encourage creativity, research, and development in emerging technologies like renewable energy, automation, and smart grids. 3. Industry Readiness: Establish collaborations with industries to bridge the gap between theoretical knowledge and real-world applications. 4. Ethical & Sustainable Solutions: Instill ethical values, environmental consciousness, and responsibility in students to develop sustainable engineering solutions. 5.Lifelong Learning: Promote adaptability to technological advancements and inspire students for continuous learning and professional growth",
            description="EEE includes power systems, electronics, and smart grids..."
        ),
        Branch(
            branch_code="ECE01",
            branch_name="Electronics & Communication Engineering",
            vision="To be a center of excellence in Electronics and Communication Engineering, driving innovation, research, and technological advancements to develop skilled professionals who contribute to the growth of modern communication systems and digital transformation.",
            mission="1. Quality Education: Provide a strong foundation in electronics, communication, and embedded systems through a well-structured curriculum and hands-on learning. 2. Research & Innovation: Foster innovation in wireless communication, VLSI, IoT, artificial intelligence, and signal processing to address global challenges. 3. Industry Collaboration: Establish strong industry partnerships to offer students real-world exposure through internships, projects, and skill development programs.4. Ethical & Sustainable Technology: Instill ethical values, environmental consciousness, and responsibility in students to develop energy-efficient and sustainable electronic solutions. 5. Lifelong Learning: Encourage adaptability to emerging technologies and continuous learning for professional excellence.",
            description="ECE focuses on telecommunications, signal processing, and chip design..."
        ),
        Branch(
            branch_code="EIE01",
            branch_name="Electronics and Instrumention Engineering",
            vision="To be a center of excellence in Electronics, Instrumentation & Control Engineering, driving innovation, research, and technological advancements to develop skilled professionals capable of designing intelligent automation and measurement systems for industrial and societal needs.",
            mission="1. Quality Education: Provide a strong foundation in electronics, sensors, automation, and control systems through a comprehensive curriculum and practical exposure. 2. Research & Innovation: Encourage innovation in robotics, process automation, IoT, AI-driven instrumentation, and smart sensor technology. 3. Industry Collaboration: Establish strong industry partnerships to bridge the gap between academia and industrial applications through internships and hands-on projects. 4. Sustainability & Ethics: Promote sustainable and energy-efficient control systems while instilling ethical values and safety standards in engineering practices. 5. Lifelong Learning: Prepare students for continuous learning and adaptability to emerging automation, industrial IoT, and smart control technologies",
            description="AIDS focuses on AI, ML, big data, and neural networks..."
        ),
        Branch(
            branch_code="AT01",
            branch_name="Automobile Engineering",
            vision="To be a center of excellence in Automobile Engineering, fostering innovation, research, and technological advancements to develop sustainable, efficient, and smart mobility solutions for the future.",
            mission="1. Quality Education: Provide a strong foundation in automotive design, manufacturing, and maintenance through a well-structured curriculum and practical exposure. 2. Research & Innovation: Encourage advancements in electric vehicles (EVs), autonomous driving, alternative fuels, and smart transportation systems. 3. Industry Collaboration: Establish partnerships with leading automobile industries to offer hands-on training, internships, and real-world project experiences. 4. Sustainability & Ethics: Promote eco-friendly and energy-efficient vehicle technologies while instilling professional ethics and road safety awareness. 5. Lifelong Learning: Equip students with skills to adapt to emerging automotive trends, AI-driven mobility, and Industry 4.0 innovations.",
            description="AE covers automobile design, electric vehicles, and transportation systems..."
        ),
        Branch(
            branch_code="ADFT01",
            branch_name="Apparel Design and Fabrication Technology",
            vision="To be a center of excellence in Apparel Design & Fabrication Technology, fostering innovation, creativity, and sustainable fashion solutions to meet global industry standards and enhance societal well-being.",
            mission="1. Quality Education: Provide a strong foundation in fashion design, textile technology, and garment manufacturing through a well-structured curriculum and hands-on training. 2. Research & Innovation: Encourage creativity and technological advancements in smart textiles, sustainable fashion, and automated garment production. 3. Industry Collaboration: Develop strong partnerships with leading fashion brands and textile industries to enhance practical exposure, internships, and real-world projects. 4. Sustainability & Ethics: Promote eco-friendly fabrics, ethical production practices, and sustainable apparel solutions to reduce environmental impact. 5. Lifelong Learning: Prepare students for global fashion trends, digital textile innovation, and entrepreneurship in the apparel industry.",
            description="MECH covers robotics, control systems, and industrial automation..."
        ),
        Branch(
            branch_code="SH01",
            branch_name="Science and Humanities",
            vision="To cultivate a deep understanding of human culture, ethics, and communication, empowering students with critical thinking, creativity, and social responsibility for a well-rounded professional and personal life.",
            mission="1. Holistic Education: Provide a strong foundation in language, ethics, sociology, and psychology to enhance personal and professional growth. 2. Effective Communication: Develop verbal and written communication skills to prepare students for diverse careers in media, business, education, and public service. 3. Ethical & Social Responsibility: Instill values of integrity, inclusivity, and sustainability to promote responsible citizenship. 4. Interdisciplinary Learning: Encourage the integration of humanities with science, technology, and management for well-rounded knowledge. 5. Lifelong Learning & Leadership: Prepare students for continuous learning, leadership roles, and adaptability to global societal changes.",
            description="AE deals with aircraft design, propulsion, and aerodynamics..."
        ),
    ]
    for branch_data in branches:
        branch = Branch.query.filter_by(branch_code=branch_data.branch_code).first()
        if branch:
            branch.description = branch_data["description"]
            branch.vision = branch_data["vision"]
            branch.mission = branch_data["mission"]
        else:
            if isinstance(branch_data, dict):
                new_branch = Branch(**branch_data)
            else:
                new_branch = Branch(
                    branch_code=branch_data.branch_code,
                    branch_name=branch_data.branch_name,
                    description=branch_data.description,
                    vision=branch_data.vision,
                    mission=branch_data.mission
                )

            db.session.add(new_branch)

    db.session.commit()
    print("Branch details updated successfully!")
