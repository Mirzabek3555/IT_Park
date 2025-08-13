// Main JavaScript for Tuproqqal'a IT Park

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add fade-in animation to cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card, .leaderboard-item').forEach(el => {
        observer.observe(el);
    });

    // Test timer functionality
    if (document.getElementById('test-timer')) {
        initializeTestTimer();
    }

    // Test submission functionality
    if (document.getElementById('test-form')) {
        initializeTestSubmission();
    }
});

// Test Timer Function
function initializeTestTimer() {
    const timerElement = document.getElementById('test-timer');
    const timeLimit = parseInt(timerElement.dataset.timeLimit) * 60; // Convert to seconds
    let timeLeft = timeLimit;
    
    function updateTimer() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        
        timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        if (timeLeft <= 0) {
            // Auto-submit test when time runs out
            if (document.getElementById('test-form')) {
                document.getElementById('test-form').submit();
            }
            return;
        }
        
        timeLeft--;
        setTimeout(updateTimer, 1000);
    }
    
    updateTimer();
}

// Test Submission Function
function initializeTestSubmission() {
    const testForm = document.getElementById('test-form');
    const submitBtn = document.getElementById('submit-test');
    const progressBar = document.getElementById('test-progress');
    
    if (!testForm || !submitBtn) return;
    
    // Track answered questions
    let answeredQuestions = new Set();
    
    // Update progress bar
    function updateProgress() {
        const totalQuestions = document.querySelectorAll('.test-question').length;
        const progress = (answeredQuestions.size / totalQuestions) * 100;
        
        if (progressBar) {
            progressBar.style.width = progress + '%';
            progressBar.textContent = Math.round(progress) + '%';
        }
    }
    
    // Handle answer selection
    document.querySelectorAll('.test-answer').forEach(answer => {
        answer.addEventListener('click', function() {
            const questionId = this.dataset.questionId;
            const answerId = this.dataset.answerId;
            
            // Remove previous selection for this question
            document.querySelectorAll(`[data-question-id="${questionId}"]`).forEach(prev => {
                prev.classList.remove('selected');
            });
            
            // Select current answer
            this.classList.add('selected');
            
            // Update answered questions
            answeredQuestions.add(questionId);
            updateProgress();
        });
    });
    
    // Handle text input for coding/logic questions
    document.querySelectorAll('.test-text-answer').forEach(input => {
        input.addEventListener('input', function() {
            const questionId = this.dataset.questionId;
            
            if (this.value.trim()) {
                answeredQuestions.add(questionId);
            } else {
                answeredQuestions.delete(questionId);
            }
            updateProgress();
        });
    });
    
    // Form submission
    testForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (answeredQuestions.size === 0) {
            alert('Iltimos, kamida bitta savolga javob bering!');
            return;
        }
        
        // Show loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Yuborilmoqda...';
        
        // Collect answers
        const answers = [];
        
        document.querySelectorAll('.test-question').forEach(question => {
            const questionId = question.dataset.questionId;
            const selectedAnswer = question.querySelector('.test-answer.selected');
            const textAnswer = question.querySelector('.test-text-answer');
            
            const answerData = {
                question_id: questionId
            };
            
            if (selectedAnswer) {
                answerData.selected_answer_id = selectedAnswer.dataset.answerId;
            }
            
            if (textAnswer && textAnswer.value.trim()) {
                answerData.text_answer = textAnswer.value.trim();
            }
            
            answers.push(answerData);
        });
        
        // Calculate time taken
        const timeTaken = parseInt(document.getElementById('test-timer').dataset.timeLimit) * 60 - 
                         (parseInt(document.getElementById('test-timer').textContent.split(':')[0]) * 60 + 
                          parseInt(document.getElementById('test-timer').textContent.split(':')[1]));
        
        // Submit data
        fetch(testForm.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                answers: answers,
                time_taken: timeTaken
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                alert('Xatolik yuz berdi: ' + data.error);
                submitBtn.disabled = false;
                submitBtn.innerHTML = 'Testni tugatish';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Xatolik yuz berdi. Iltimos, qaytadan urinib ko\'ring.');
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Testni tugatish';
        });
    });
    
    // Initialize progress
    updateProgress();
}

// Utility function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Search functionality for test list
function initializeTestSearch() {
    const searchInput = document.getElementById('test-search');
    const testCards = document.querySelectorAll('.test-card');
    
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        
        testCards.forEach(card => {
            const title = card.querySelector('.test-title').textContent.toLowerCase();
            const description = card.querySelector('.test-description').textContent.toLowerCase();
            const category = card.querySelector('.test-category').textContent.toLowerCase();
            
            if (title.includes(searchTerm) || description.includes(searchTerm) || category.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

// Filter functionality for test list
function initializeTestFilters() {
    const categoryFilter = document.getElementById('category-filter');
    const subjectFilter = document.getElementById('subject-filter');
    const testCards = document.querySelectorAll('.test-card');
    
    function applyFilters() {
        const selectedCategory = categoryFilter ? categoryFilter.value : '';
        const selectedSubject = subjectFilter ? subjectFilter.value : '';
        
        testCards.forEach(card => {
            const cardCategory = card.dataset.category;
            const cardSubject = card.dataset.subject;
            
            const categoryMatch = !selectedCategory || cardCategory === selectedCategory;
            const subjectMatch = !selectedSubject || cardSubject === selectedSubject;
            
            if (categoryMatch && subjectMatch) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }
    
    if (categoryFilter) {
        categoryFilter.addEventListener('change', applyFilters);
    }
    
    if (subjectFilter) {
        subjectFilter.addEventListener('change', applyFilters);
    }
}

// Initialize search and filters if elements exist
document.addEventListener('DOMContentLoaded', function() {
    initializeTestSearch();
    initializeTestFilters();
});
