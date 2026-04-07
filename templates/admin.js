// Store skills arrays
let mandatorySkills = [];
let optionalSkills = [];

// DOM Elements
const jobForm = document.getElementById('jobForm');
const mandatorySkillInput = document.getElementById('mandatorySkillInput');
const optionalSkillInput = document.getElementById('optionalSkillInput');
const mandatorySkillsTags = document.getElementById('mandatorySkillsTags');
const optionalSkillsTags = document.getElementById('optionalSkillsTags');
const certificationEnabled = document.getElementById('certificationEnabled');
const certificationWeight = document.getElementById('certificationWeight');
const certWeightValue = document.getElementById('certWeightValue');
const certWeightGroup = document.getElementById('certWeightGroup');
const jobDescription = document.getElementById('jobDescription');
const descCharCount = document.getElementById('descCharCount');
const previewSection = document.getElementById('previewSection');
const jsonPreview = document.getElementById('jsonPreview');
const successModal = document.getElementById('successModal');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Add event listeners
    mandatorySkillInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            addMandatorySkill();
        }
    });

    optionalSkillInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            addOptionalSkill();
        }
    });

    // Certification toggle
    certificationEnabled.addEventListener('change', () => {
        if (certificationEnabled.checked) {
            certWeightGroup.classList.remove('disabled');
        } else {
            certWeightGroup.classList.add('disabled');
            certificationWeight.value = 0;
            certWeightValue.textContent = '0%';
        }
    });

    // Certification weight slider
    certificationWeight.addEventListener('input', () => {
        certWeightValue.textContent = certificationWeight.value + '%';
    });

    // Character count for description
    jobDescription.addEventListener('input', () => {
        descCharCount.textContent = jobDescription.value.length;
    });

    // Form submission
    jobForm.addEventListener('submit', handleSubmit);

    // Initialize disabled state
    certWeightGroup.classList.add('disabled');
});

// Add mandatory skill
function addMandatorySkill() {
    const skill = mandatorySkillInput.value.trim();
    if (skill && !mandatorySkills.includes(skill.toLowerCase())) {
        mandatorySkills.push(skill.toLowerCase());
        renderMandatorySkills();
        mandatorySkillInput.value = '';
        mandatorySkillInput.focus();
    }
}

// Add optional skill
function addOptionalSkill() {
    const skill = optionalSkillInput.value.trim();
    if (skill && !optionalSkills.includes(skill.toLowerCase())) {
        optionalSkills.push(skill.toLowerCase());
        renderOptionalSkills();
        optionalSkillInput.value = '';
        optionalSkillInput.focus();
    }
}

// Remove mandatory skill
function removeMandatorySkill(skill) {
    mandatorySkills = mandatorySkills.filter(s => s !== skill);
    renderMandatorySkills();
}

// Remove optional skill
function removeOptionalSkill(skill) {
    optionalSkills = optionalSkills.filter(s => s !== skill);
    renderOptionalSkills();
}

// Render mandatory skills tags
function renderMandatorySkills() {
    mandatorySkillsTags.innerHTML = mandatorySkills.map(skill => `
        <span class="skill-tag">
            ${capitalizeFirst(skill)}
            <button type="button" class="remove-skill" onclick="removeMandatorySkill('${skill}')">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
            </button>
        </span>
    `).join('');
    
    document.getElementById('mandatorySkills').value = JSON.stringify(mandatorySkills);
}

// Render optional skills tags
function renderOptionalSkills() {
    optionalSkillsTags.innerHTML = optionalSkills.map(skill => `
        <span class="skill-tag">
            ${capitalizeFirst(skill)}
            <button type="button" class="remove-skill" onclick="removeOptionalSkill('${skill}')">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
            </button>
        </span>
    `).join('');
    
    document.getElementById('optionalSkills').value = JSON.stringify(optionalSkills);
}

// Capitalize first letter
function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Get form data as JSON
function getFormData() {
    return {
        title: document.getElementById('jobTitle').value.trim(),
        description: jobDescription.value.trim(),
        mandatory_skills: mandatorySkills,
        optional_skills: optionalSkills,
        certification_enabled: certificationEnabled.checked,
        certification_weight: certificationEnabled.checked ? parseInt(certificationWeight.value) : 0
    };
}

// Preview JSON
function previewJSON() {
    const data = getFormData();
    jsonPreview.textContent = JSON.stringify(data, null, 2);
    previewSection.style.display = 'block';
    previewSection.scrollIntoView({ behavior: 'smooth' });
}

// Reset form
function resetForm() {
    jobForm.reset();
    mandatorySkills = [];
    optionalSkills = [];
    renderMandatorySkills();
    renderOptionalSkills();
    certWeightGroup.classList.add('disabled');
    certWeightValue.textContent = '0%';
    descCharCount.textContent = '0';
    previewSection.style.display = 'none';
}

// Handle form submission
function handleSubmit(e) {
    e.preventDefault();
    
    const data = getFormData();
    
    // Validation
    if (!data.title) {
        alert('Please enter a job title');
        return;
    }
    
    if (data.description.length < 20) {
        alert('Please enter a more detailed job description (at least 20 characters)');
        return;
    }
    
    if (mandatorySkills.length === 0) {
        alert('Please add at least one mandatory skill');
        return;
    }
    
    // Log the data (you can replace this with your API call)
    console.log('Job Description Data:', data);
    console.log('JSON:', JSON.stringify(data, null, 2));
    
    // Show success modal
    successModal.classList.add('active');
    
    // Here you would typically send data to your backend:
    // fetch('/api/jobs', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify(data)
    // })
    // .then(response => response.json())
    // .then(result => {
    //     successModal.classList.add('active');
    // })
    // .catch(error => {
    //     console.error('Error:', error);
    //     alert('Failed to save job description');
    // });
}

// Close modal
function closeModal() {
    successModal.classList.remove('active');
    resetForm();
}

// View jobs (placeholder)
function viewJobs() {
    successModal.classList.remove('active');
    alert('This would navigate to the jobs list page');
    // window.location.href = '/jobs';
}
