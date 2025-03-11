from app import db, app
from models import Branch
with app.app_context():
    branches = [
        Branch(
            branch_code="IST01",
            branch_name="Information Science & Technology",
            vision="The vision of Information Science is focuses on various aspects of data, Information. It covers the design and development to meet the needs of Global Information society. Imparting quality technical education and preparing professionals to meet Information Technological (IT) challenges globally.",
            mission="The mission of Information Science is to provide teaching / learning facility, quality technical Education and encourage students to pursue higher education for future growth. Prepare highly skilled Information Science Engineers through best practices. Encourage students to pursue Higher Education for further growth in the learning process and to promote research in the frontier areas of Information technology. Educate students to take up social and professional responsibilities with Ethical values for the betterment of the society.",
            description="This branch covers programming, networking, AI, and software development"
        ),
        Branch(
            branch_code="CSE01",
            branch_name="Computer Science & Engineering",
            vision="To be a department of Excellence in Technical Education and to foster the students in to globally competent professionals with expertise in software development, research and ethical values./n",
            mission="Provide the ambience to become industry ready professionals, Researchers and Entrepreneurs by offering courses on cutting edge technology and advanced software. To provide a conducing environment to enhance problem solving skills. leadership qualities and team spirit. Import high quality experimental learning to get expertise in modern software tools and to cater to the real time requirements of the industry. Inculcate problem solving and team building skills and promote lifelong learning with a sense of social and ethical responsibilities./n",
            description="CSE focuses on software, hardware, AI, and cloud computing"
        ),
        Branch(
            branch_code="ME01",
            branch_name="Mechanical Engineering",
            vision="To be at the forefront in Mechanical education relevant to the needs of industry and society",
            mission="Educate students in practical aspects to meet industry requirements. Empower students with technical knowledge to pursue higher education. To instill interpersonal skills and sense of ethical responsibilities",
            description="ME deals with design, automation, and industrial machinery"
        ),
        Branch(
            branch_code="CE01",
            branch_name="Civil Engineering",
            vision="To impart knowledge and Excellence in Civil Engineering field with global perspectives and make them ethically strong to bring good reputation to the Institute and the Nation.",
            mission="To train and prepare every student as a qualified and responsible Civil Engineers of high caliber, precise technical skills and ethical values to serve the Society",
            description="CE covers infrastructure design, construction, and urban planning"
        ),
        Branch(
            branch_code="EEE01",
            branch_name="Electrical & Electronics Engineering",
            vision="To be a center of excellence in Electrical and Electronics Engineering, fostering innovation, research, and sustainable technological advancements to meet global challenges and contribute to societal development.",
            mission="To impart excellent technical knowledge and practical skills to enable the students to apply their knowledge to identify problems and provide solutions. To nurture ethical values to be good engineers. To promote a lifelong learning mindset to contribute to developmental activities in society.",
            description="EEE includes power systems, electronics, and smart grids"
        ),
        Branch(
            branch_code="ECE01",
            branch_name="Electronics & Communication Engineering",
            vision="To Fecilitate the new generation with ample opportunities, appropriate guidance, enough space to excel in the field of technology to contribute to the society in creating a fulfilled... progressive and prosperous tomorrow....",
            mission="Making the students to understand the meaning. the importance and the essence of the program by giving an insight about various subjects available in the branch of Electronics. Encouraging a student to think more than the syllabus by taking the teaching beyond the boundary of a classroom. Adopting the methods of Listen and explain, learn through hands-on, practice and establish. Promoting the students to think outside the box and challenging them to come up with indigenous project models. Cultural, social, sports and Industrial participation to make the students competent and confident individuals. Providing yoga and personality development activities.",
            description="ECE focuses on telecommunications, signal processing, and chip design"
        ),
        Branch(
            branch_code="EIE01",
            branch_name="Electronics Instrumentation And Control Engineering",
            vision="Achieving Excellence in the area of Instrumentation and Control Engineering to meet the Industrial and societal needs.",
            mission="To impart technical knowledge through systematic teaching and learning process in interaction with industry and alumini. To enhance the employability skills and develop industry ready students.  To provide extension service to rural society and instill ethical values among the students. To prepare and built the ability for independent and lifelong learning by enhancing the knowledge base and skills necessary to contribute to the improvement of their profession and Community.",
            description="EIE is a technical course focusing on the principles and operation of measuring instruments, encompassing electronics circuits, control systems, and data acquisition, primarily used to design and monitor automated systems in various industrial settings"
        ),
        Branch(
            branch_code="AT01",
            branch_name="Automobile Engineering",
            vision="Produce productive and adept technicians with social and ethical values for global requirement within the automotive field through excellent technical education.",
            mission="To provide quality education incorporating with changing trends in Automobile. To enchance student's practical knowledge and employability through industry institute interaction.  To inculcate professional skills and social values among the students through curricular, co-curricular and extra-curricular activity.",
            description="AE covers automobile design, electric vehicles, and transportation systems"
        ),
        Branch(
            branch_code="ADFT01",
            branch_name="Apparel Design and Fabrication Technology",
            vision="Catering individual creativity to the world of fashion, to encourage entrepreneurship with the aim of creating employment.",
            mission="To Empower Students to have Satisfying and Truth career in Fashion Industry. To Equip students with basic Knowledge of Fashion Industry which would in turn help them pursue Higher Education. To Empower Students with ample Knowledge to set up new start-ups or self -help groups. To Encourage Entrepreneurial skills and Technical Knowledge for National and International Fashion centers and Apparel Industry",
            description="ADFT is the study of designing clothing and accessories, along with the techniques and technologies involved in fabricating them"
        ),
        Branch(
            branch_code="SH01",
            branch_name="Science and Humanities",
            vision="To cultivate a deep understanding of human culture, ethics, and communication, empowering students with critical thinking, creativity, and social responsibility for a well-rounded professional and personal life.",
            mission="Holistic Education: Provide a strong foundation in language, ethics, sociology, and psychology to enhance personal and professional growth.Effective Communication: Develop verbal and written communication skills to prepare students for diverse careers in media, business, education, and public service.Ethical & Social Responsibility: Instill values of integrity, inclusivity, and sustainability to promote responsible citizenship.Interdisciplinary Learning: Encourage the integration of humanities with science, technology, and management for well-rounded knowledge.Lifelong Learning & Leadership: Prepare students for continuous learning, leadership roles, and adaptability to global societal changes.",
            description="Science and Humanities is a primal department which consists of Chemistry, Physics, Mathematics and English disciplines"
        ),
        Branch(
            branch_code="OI01",
            branch_name="Office Info",
            vision="To create a centralized and efficient digital platform for managing all administrative and academic operations, ensuring seamless communication and data management across all branches.",
            mission="To provide a secure and user-friendly system for managing student records, staff details, and administrative tasks.To enhance transparency and accessibility of important information for students, faculty, and staff. To implement a role-based access control system for better data security and management.To facilitate quick decision-making through real-time data access and updates",
            description="Office Info is the central admin panel for managing student records, staff details, fee structures, course updates, and announcements. It provides secure access for admins to oversee and update data across all branches efficiently."
        )
    ]
    for branch_data in branches:
        branch = Branch.query.filter_by(branch_code=branch_data.branch_code).first()
        if branch:
            branch.description = branch_data.description
            branch.vision = branch_data.vision
            branch.mission = branch_data.mission
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
