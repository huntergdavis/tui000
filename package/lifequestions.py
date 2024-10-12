import random

class LifeEventQuestions:

    # Store 100 questions and their respective choices
    questions = [
        {
            "question": "1. You walk into a car dealership. The dealer is friendly, and you enjoy the experience. Which color car do you choose?",
            "choices": [('a', 'Red'), ('b', 'Green'), ('c', 'Blue'), ('d', 'Yellow')]
        },
        {
            "question": "2. You receive job offers from two companies. One offers higher pay, the other better work-life balance. Which do you choose?",
            "choices": [('a', 'Higher pay'), ('b', 'Work-life balance'), ('c', 'Negotiate with both'), ('d', 'Start your own business')]
        },
        {
            "question": "3. You inherit a large sum of money from a distant relative. What do you do first?",
            "choices": [('a', 'Invest it'), ('b', 'Buy a house'), ('c', 'Travel the world'), ('d', 'Donate to charity')]
        },
        {
            "question": "4. You're planning a vacation with friends, but they want to go somewhere you're not interested in. What do you do?",
            "choices": [('a', 'Go anyway'), ('b', 'Suggest a different place'), ('c', 'Stay home'), ('d', 'Plan a solo trip elsewhere')]
        },
        {
            "question": "5. You decide to start a new hobby. Which one do you choose?",
            "choices": [('a', 'Painting'), ('b', 'Gardening'), ('c', 'Playing an instrument'), ('d', 'Learning a language')]
        },
        {
            "question": "6. A friend asks you to help them move on your only day off. What do you do?",
            "choices": [('a', 'Help them'), ('b', 'Politely decline'), ('c', 'Offer partial help'), ('d', 'Hire movers for them')]
        },
        {
            "question": "7. You get a chance to relocate to a new city for a job promotion. What do you do?",
            "choices": [('a', 'Accept'), ('b', 'Decline'), ('c', 'Ask for remote work'), ('d', 'Negotiate terms')]
        },
        {
            "question": "8. You find out that your best friend is moving across the country. How do you react?",
            "choices": [('a', 'Throw a farewell party'), ('b', 'Plan regular visits'), ('c', 'Feel sad but supportive'), ('d', 'Offer to help with the move')]
        },
        {
            "question": "9. You have an opportunity to go back to school and pursue a degree. What do you study?",
            "choices": [('a', 'Business'), ('b', 'Art and Design'), ('c', 'Computer Science'), ('d', 'Education')]
        },
        {
            "question": "10. Your company is offering a 6-month sabbatical. How do you spend it?",
            "choices": [('a', 'Travel'), ('b', 'Start a personal project'), ('c', 'Relax at home'), ('d', 'Volunteer work')]
        },
        {
            "question": "11. You decide to adopt a pet. Which animal do you choose?",
            "choices": [('a', 'Dog'), ('b', 'Cat'), ('c', 'Bird'), ('d', 'Rabbit')]
        },
        {
            "question": "12. You're considering buying a home. What type do you prefer?",
            "choices": [('a', 'Apartment'), ('b', 'Single-family house'), ('c', 'Condominium'), ('d', 'Townhouse')]
        },
        {
            "question": "13. A close family member needs financial assistance. What do you do?",
            "choices": [('a', 'Give them money'), ('b', 'Offer a loan'), ('c', 'Help them budget'), ('d', 'Politely decline')]
        },
        {
            "question": "14. You want to improve your fitness. What activity do you choose?",
            "choices": [('a', 'Join a gym'), ('b', 'Start running'), ('c', 'Yoga classes'), ('d', 'Team sports')]
        },
        {
            "question": "15. You're offered a leadership role at work. How do you respond?",
            "choices": [('a', 'Accept eagerly'), ('b', 'Decline politely'), ('c', 'Negotiate terms'), ('d', 'Request time to consider')]
        },
        {
            "question": "16. Your friend invites you to a networking event. What do you do?",
            "choices": [('a', 'Attend and network'), ('b', 'Decline the invitation'), ('c', 'Suggest meeting afterward'), ('d', 'Offer to help organize')]
        },
        {
            "question": "17. You notice a coworker taking credit for your work. How do you handle it?",
            "choices": [('a', 'Confront them'), ('b', 'Speak to your manager'), ('c', 'Let it go'), ('d', 'Document your contributions')]
        },
        {
            "question": "18. You're feeling burnt out. What action do you take?",
            "choices": [('a', 'Take a vacation'), ('b', 'Consult a therapist'), ('c', 'Change your routine'), ('d', 'Ignore it and continue')]
        },
        {
            "question": "19. A neighbor plays loud music late at night. How do you address it?",
            "choices": [('a', 'Talk to them politely'), ('b', 'Call the authorities'), ('c', 'Ignore it'), ('d', 'Leave an anonymous note')]
        },
        {
            "question": "20. You want to volunteer in your community. Which cause do you choose?",
            "choices": [('a', 'Environmental cleanup'), ('b', 'Homeless shelters'), ('c', 'Animal rescue'), ('d', 'Youth mentorship')]
        },
        {
            "question": "21. You discover a passion for cooking. What cuisine do you focus on?",
            "choices": [('a', 'Italian'), ('b', 'Japanese'), ('c', 'Mexican'), ('d', 'Mediterranean')]
        },
        {
            "question": "22. You decide to start investing. What do you invest in?",
            "choices": [('a', 'Stocks'), ('b', 'Real estate'), ('c', 'Bonds'), ('d', 'Cryptocurrency')]
        },
        {
            "question": "23. Your car breaks down beyond repair. What do you do?",
            "choices": [('a', 'Buy a new car'), ('b', 'Use public transportation'), ('c', 'Carpool with coworkers'), ('d', 'Bike to work')]
        },
        {
            "question": "24. You have free time on weekends. How do you spend it?",
            "choices": [('a', 'Reading'), ('b', 'Outdoor activities'), ('c', 'Watching movies'), ('d', 'Socializing with friends')]
        },
        {
            "question": "25. You're invited to a friend's wedding abroad. Do you attend?",
            "choices": [('a', 'Yes, definitely'), ('b', 'No, too expensive'), ('c', 'Send a gift instead'), ('d', 'Attend virtually')]
        },
        {
            "question": "26. You want to reduce your environmental impact. What do you change?",
            "choices": [('a', 'Recycle more'), ('b', 'Use public transport'), ('c', 'Adopt a plant-based diet'), ('d', 'Install solar panels')]
        },
        {
            "question": "27. You feel the need for a career change. What field do you consider?",
            "choices": [('a', 'Healthcare'), ('b', 'Technology'), ('c', 'Education'), ('d', 'Entrepreneurship')]
        },
        {
            "question": "28. You win a free class at a local community center. What do you choose?",
            "choices": [('a', 'Dance'), ('b', 'Pottery'), ('c', 'Photography'), ('d', 'Culinary arts')]
        },
        {
            "question": "29. Your friend's birthday is coming up. How do you celebrate?",
            "choices": [('a', 'Throw a surprise party'), ('b', 'Plan a dinner out'), ('c', 'Get a thoughtful gift'), ('d', 'Send a heartfelt message')]
        },
        {
            "question": "30. You want to learn a new language. Which one do you choose?",
            "choices": [('a', 'Spanish'), ('b', 'French'), ('c', 'Mandarin Chinese'), ('d', 'German')]
        },
        {
            "question": "31. You decide to write a book. What genre do you choose?",
            "choices": [('a', 'Fiction'), ('b', 'Non-fiction'), ('c', 'Biography'), ('d', 'Science Fiction')]
        },
        {
            "question": "32. You consider starting a small business. What type do you start?",
            "choices": [('a', 'Cafe'), ('b', 'Online store'), ('c', 'Consulting firm'), ('d', 'Handmade crafts')]
        },
        {
            "question": "33. You're offered a chance to teach a class. What subject do you teach?",
            "choices": [('a', 'Math'), ('b', 'Art'), ('c', 'History'), ('d', 'Computer Science')]
        },
        {
            "question": "34. You want to adopt a healthier diet. What approach do you take?",
            "choices": [('a', 'Go vegetarian'), ('b', 'Cook more at home'), ('c', 'Consult a nutritionist'), ('d', 'Join a meal plan service')]
        },
        {
            "question": "35. A new hobby catches your eye. Which do you pick up?",
            "choices": [('a', 'Knitting'), ('b', 'Chess'), ('c', 'Rock climbing'), ('d', 'Photography')]
        },
        {
            "question": "36. You have the option to work remotely. Do you take it?",
            "choices": [('a', 'Yes, full-time remote'), ('b', 'No, prefer office'), ('c', 'Hybrid model'), ('d', 'Occasional remote days')]
        },
        {
            "question": "37. You want to reconnect with an old friend. How do you reach out?",
            "choices": [('a', 'Call them'), ('b', 'Send a message'), ('c', 'Plan a meetup'), ('d', 'Email them')]
        },
        {
            "question": "38. You find a lost wallet on the street. What do you do?",
            "choices": [('a', 'Return it to the owner'), ('b', 'Hand it to the police'), ('c', 'Leave it there'), ('d', 'Look for ID to contact them')]
        },
        {
            "question": "39. You're interested in improving your public speaking skills. What do you do?",
            "choices": [('a', 'Join a speaking club'), ('b', 'Take a class'), ('c', 'Practice on your own'), ('d', 'Avoid public speaking')]
        },
        {
            "question": "40. You decide to plant a garden. What do you grow?",
            "choices": [('a', 'Vegetables'), ('b', 'Flowers'), ('c', 'Herbs'), ('d', 'Fruit trees')]
        },
        {
            "question": "41. You're invited to participate in a charity event. Which role do you take?",
            "choices": [('a', 'Volunteer'), ('b', 'Donor'), ('c', 'Organizer'), ('d', 'Participant')]
        },
        {
            "question": "42. You want to reduce stress in your life. What method do you try?",
            "choices": [('a', 'Meditation'), ('b', 'Exercise'), ('c', 'Time management'), ('d', 'Hobbies')]
        },
        {
            "question": "43. You have the opportunity to mentor someone. Do you accept?",
            "choices": [('a', 'Yes, happily'), ('b', 'No, not interested'), ('c', 'Maybe, if time allows'), ('d', 'Refer them to someone else')]
        },
        {
            "question": "44. You're considering getting a pet. Do you adopt or buy?",
            "choices": [('a', 'Adopt from a shelter'), ('b', 'Buy from a breeder'), ('c', 'Pet-sit instead'), ('d', 'Decide against getting a pet')]
        },
        {
            "question": "45. You find a new favorite author. What do you do?",
            "choices": [('a', 'Read all their books'), ('b', 'Attend a book signing'), ('c', 'Recommend to friends'), ('d', 'Join a fan club')]
        },
        {
            "question": "46. You're offered free tickets to a concert. Do you go?",
            "choices": [('a', 'Yes, love live music'), ('b', 'No, not interested'), ('c', 'Give tickets to someone else'), ('d', 'Sell the tickets')]
        },
        {
            "question": "47. You want to improve your home. What project do you undertake?",
            "choices": [('a', 'Renovate the kitchen'), ('b', 'Landscape the yard'), ('c', 'Add a home office'), ('d', 'Redecorate the living room')]
        },
        {
            "question": "48. A new technology interests you. How do you learn more?",
            "choices": [('a', 'Take an online course'), ('b', 'Read articles'), ('c', 'Attend a workshop'), ('d', 'Experiment on your own')]
        },
        {
            "question": "49. You're feeling adventurous with food. What do you try?",
            "choices": [('a', 'A new restaurant'), ('b', 'Cooking exotic recipes'), ('c', 'Attend a food festival'), ('d', 'Try street food')]
        },
        {
            "question": "50. You decide to get involved in local politics. What role do you take?",
            "choices": [('a', 'Run for office'), ('b', 'Campaign volunteer'), ('c', 'Community organizer'), ('d', 'Voter education')]
        },
        {
            "question": "51. You want to challenge yourself physically. What do you attempt?",
            "choices": [('a', 'Marathon'), ('b', 'Mountain climbing'), ('c', 'Triathlon'), ('d', 'Join a sports league')]
        },
        {
            "question": "52. You're interested in art. How do you explore this interest?",
            "choices": [('a', 'Visit museums'), ('b', 'Take art classes'), ('c', 'Collect art'), ('d', 'Support local artists')]
        },
        {
            "question": "53. A family member suggests a reunion. How do you respond?",
            "choices": [('a', 'Help plan it'), ('b', 'Attend eagerly'), ('c', 'Decline politely'), ('d', 'Suggest a virtual meetup')]
        },
        {
            "question": "54. You consider furthering your education. What level do you pursue?",
            "choices": [('a', 'Bachelor’s degree'), ('b', 'Master’s degree'), ('c', 'Doctorate'), ('d', 'Professional certification')]
        },
        {
            "question": "55. You want to become more organized. What tool do you use?",
            "choices": [('a', 'Planner'), ('b', 'Digital app'), ('c', 'Bullet journal'), ('d', 'Hire a professional organizer')]
        },
        {
            "question": "56. You're thinking about your retirement plans. What do you focus on?",
            "choices": [('a', 'Financial savings'), ('b', 'Location'), ('c', 'Activities and hobbies'), ('d', 'Health and wellness')]
        },
        {
            "question": "57. You decide to reduce clutter at home. How do you proceed?",
            "choices": [('a', 'Donate items'), ('b', 'Hold a garage sale'), ('c', 'Throw away unnecessary items'), ('d', 'Organize and store')]
        },
        {
            "question": "58. You receive an unexpected day off. How do you spend it?",
            "choices": [('a', 'Relax at home'), ('b', 'Catch up on errands'), ('c', 'Visit friends'), ('d', 'Start a mini-project')]
        },
        {
            "question": "59. You want to enhance your wardrobe. What do you do?",
            "choices": [('a', 'Go shopping'), ('b', 'Hire a stylist'), ('c', 'Revamp existing clothes'), ('d', 'Attend a fashion workshop')]
        },
        {
            "question": "60. You're considering getting involved in a cause. Which one?",
            "choices": [('a', 'Environmental protection'), ('b', 'Human rights'), ('c', 'Health awareness'), ('d', 'Education reform')]
        },
        {
            "question": "61. A friend recommends a new podcast. Do you listen?",
            "choices": [('a', 'Yes, immediately'), ('b', 'Add it to your list'), ('c', 'Not interested'), ('d', 'Recommend one back')]
        },
        {
            "question": "62. You feel disconnected from nature. What do you do?",
            "choices": [('a', 'Go hiking'), ('b', 'Camping trip'), ('c', 'Visit a park'), ('d', 'Start gardening')]
        },
        {
            "question": "63. You're interested in learning about your ancestry. How do you proceed?",
            "choices": [('a', 'Take a DNA test'), ('b', 'Research family history'), ('c', 'Interview relatives'), ('d', 'Join a genealogy group')]
        },
        {
            "question": "64. You want to improve your financial literacy. What steps do you take?",
            "choices": [('a', 'Read books on finance'), ('b', 'Attend workshops'), ('c', 'Hire a financial advisor'), ('d', 'Take online courses')]
        },
        {
            "question": "65. You have an idea for a mobile app. What do you do?",
            "choices": [('a', 'Learn to code'), ('b', 'Hire a developer'), ('c', 'Pitch to investors'), ('d', 'Survey potential users')]
        },
        {
            "question": "66. You notice a local issue that needs attention. How do you act?",
            "choices": [('a', 'Start a petition'), ('b', 'Inform local authorities'), ('c', 'Organize a community meeting'), ('d', 'Address it yourself')]
        },
        {
            "question": "67. You're offered an opportunity to study abroad. Do you take it?",
            "choices": [('a', 'Yes, excitedly'), ('b', 'No, stay home'), ('c', 'Consider a short-term program'), ('d', 'Research before deciding')]
        },
        {
            "question": "68. You decide to improve your work-life balance. What change do you make?",
            "choices": [('a', 'Set boundaries'), ('b', 'Reduce work hours'), ('c', 'Prioritize self-care'), ('d', 'Seek flexible arrangements')]
        },
        {
            "question": "69. You want to experience a cultural festival. Which do you attend?",
            "choices": [('a', 'Carnival in Brazil'), ('b', 'Oktoberfest in Germany'), ('c', 'Cherry Blossom Festival in Japan'), ('d', 'Diwali in India')]
        },
        {
            "question": "70. You're inspired to create art. What medium do you choose?",
            "choices": [('a', 'Painting'), ('b', 'Sculpture'), ('c', 'Digital art'), ('d', 'Photography')]
        },
        {
            "question": "71. You wish to strengthen your relationship with family. What do you do?",
            "choices": [('a', 'Plan regular gatherings'), ('b', 'Start a family group chat'), ('c', 'Organize a family vacation'), ('d', 'Share family history')]
        },
        {
            "question": "72. You're considering adopting a minimalist lifestyle. What's your first step?",
            "choices": [('a', 'Declutter your space'), ('b', 'Limit new purchases'), ('c', 'Simplify your schedule'), ('d', 'Reflect on values')]
        },
        {
            "question": "73. You receive a promotion at work. How do you celebrate?",
            "choices": [('a', 'Dinner with loved ones'), ('b', 'Treat yourself to something nice'), ('c', 'Share the news on social media'), ('d', 'Begin planning next goals')]
        },
        {
            "question": "74. You have a chance to learn an instrument. Which do you pick?",
            "choices": [('a', 'Guitar'), ('b', 'Piano'), ('c', 'Violin'), ('d', 'Drums')]
        },
        {
            "question": "75. You're inspired to start a blog. What's your focus?",
            "choices": [('a', 'Travel'), ('b', 'Food'), ('c', 'Technology'), ('d', 'Lifestyle')]
        },
        {
            "question": "76. You decide to improve your sleep habits. What change do you make?",
            "choices": [('a', 'Establish a bedtime routine'), ('b', 'Limit screen time before bed'), ('c', 'Invest in a better mattress'), ('d', 'Use relaxation techniques')]
        },
        {
            "question": "77. You're interested in renewable energy. How do you get involved?",
            "choices": [('a', 'Install solar panels'), ('b', 'Advocate for policy change'), ('c', 'Invest in green companies'), ('d', 'Educate others')]
        },
        {
            "question": "78. You want to improve your cooking skills. What do you do?",
            "choices": [('a', 'Take a cooking class'), ('b', 'Try new recipes'), ('c', 'Watch cooking shows'), ('d', 'Cook with friends')]
        },
        {
            "question": "79. You're considering getting a part-time job. Why?",
            "choices": [('a', 'Extra income'), ('b', 'Explore a new field'), ('c', 'Meet new people'), ('d', 'Fill free time')]
        },
        {
            "question": "80. You decide to create a personal website. What's its purpose?",
            "choices": [('a', 'Professional portfolio'), ('b', 'Blogging platform'), ('c', 'Online resume'), ('d', 'Share hobbies')]
        },
        {
            "question": "81. You find an old hobby you used to love. What do you do?",
            "choices": [('a', 'Pick it up again'), ('b', 'Teach it to others'), ('c', 'Combine it with a new hobby'), ('d', 'Reflect on past interests')]
        },
        {
            "question": "82. You feel the urge to declutter digital files. Where do you start?",
            "choices": [('a', 'Email inbox'), ('b', 'Photos'), ('c', 'Documents'), ('d', 'Apps and software')]
        },
        {
            "question": "83. You decide to create a personal budget. What method do you use?",
            "choices": [('a', 'Spreadsheet'), ('b', 'Budgeting app'), ('c', 'Envelope system'), ('d', 'Hire a financial planner')]
        },
        {
            "question": "84. You're interested in sustainable fashion. How do you participate?",
            "choices": [('a', 'Buy second-hand'), ('b', 'Support ethical brands'), ('c', 'Upcycle clothing'), ('d', 'Reduce purchases')]
        },
        {
            "question": "85. You want to improve your mental health. What step do you take?",
            "choices": [('a', 'Mindfulness practices'), ('b', 'Therapy'), ('c', 'Journaling'), ('d', 'Connect with loved ones')]
        },
        {
            "question": "86. You decide to explore your city more. What do you do?",
            "choices": [('a', 'Visit landmarks'), ('b', 'Try local restaurants'), ('c', 'Attend community events'), ('d', 'Join local tours')]
        },
        {
            "question": "87. You want to support local businesses. How do you contribute?",
            "choices": [('a', 'Shop at local stores'), ('b', 'Promote them online'), ('c', 'Attend local markets'), ('d', 'Provide feedback')]
        },
        {
            "question": "88. You're considering adopting a plant. Which do you choose?",
            "choices": [('a', 'Succulent'), ('b', 'Fern'), ('c', 'Flowering plant'), ('d', 'Herb')]
        },
        {
            "question": "89. You feel like exploring spirituality. What path do you take?",
            "choices": [('a', 'Meditation'), ('b', 'Religious study'), ('c', 'Yoga'), ('d', 'Philosophical readings')]
        },
        {
            "question": "90. You decide to document your life. How do you do it?",
            "choices": [('a', 'Daily journal'), ('b', 'Video diaries'), ('c', 'Photo albums'), ('d', 'Blogging')]
        },
        {
            "question": "91. You're inspired to give back to your alma mater. What do you do?",
            "choices": [('a', 'Donate funds'), ('b', 'Mentor students'), ('c', 'Attend alumni events'), ('d', 'Offer internships')]
        },
        {
            "question": "92. You want to make your mornings more productive. What change do you make?",
            "choices": [('a', 'Wake up earlier'), ('b', 'Plan the night before'), ('c', 'Exercise in the morning'), ('d', 'Limit distractions')]
        },
        {
            "question": "93. You consider downsizing your living space. Why?",
            "choices": [('a', 'Simplify life'), ('b', 'Save money'), ('c', 'Environmental reasons'), ('d', 'Travel more')]
        },
        {
            "question": "94. You're interested in learning about wine. How do you start?",
            "choices": [('a', 'Wine tasting events'), ('b', 'Enroll in a course'), ('c', 'Read books on wine'), ('d', 'Visit vineyards')]
        },
        {
            "question": "95. You decide to challenge yourself intellectually. What do you do?",
            "choices": [('a', 'Learn a new language'), ('b', 'Take advanced courses'), ('c', 'Join debates'), ('d', 'Solve puzzles regularly')]
        },
        {
            "question": "96. You want to improve your handwriting. What's your approach?",
            "choices": [('a', 'Practice calligraphy'), ('b', 'Write by hand more often'), ('c', 'Use handwriting guides'), ('d', 'Attend a workshop')]
        },
        {
            "question": "97. You're considering fostering animals. What do you do?",
            "choices": [('a', 'Apply to be a foster'), ('b', 'Volunteer at shelters'), ('c', 'Donate supplies'), ('d', 'Adopt instead')]
        },
        {
            "question": "98. You want to be more eco-friendly at home. What change do you make?",
            "choices": [('a', 'Compost waste'), ('b', 'Use energy-efficient appliances'), ('c', 'Collect rainwater'), ('d', 'Switch to LED lighting')]
        },
        {
            "question": "99. You decide to improve your networking skills. How do you proceed?",
            "choices": [('a', 'Attend events'), ('b', 'Join professional groups'), ('c', 'Enhance online presence'), ('d', 'Seek mentorship')]
        },
        {
            "question": "100. You consider taking a digital detox. How long do you plan?",
            "choices": [('a', 'One day'), ('b', 'One week'), ('c', 'One month'), ('d', 'Indefinitely')]
        }
    ]
    def __init__(self):
        pass

    def get_random_question():
        """Returns a random question and its associated choices."""
        return random.choice(LifeEventQuestions.questions)
