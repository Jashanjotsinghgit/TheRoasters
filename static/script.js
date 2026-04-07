// Mock data (simulating backend response)
let jobsData = [];
let selectedJobId = null;
let selectedJobData = null;

const analysisData = {
  name: "Jashan",
  semantic: 0.52,
  skill: 0.08,
  final: 0.4,
  category: "Weak Match",
  matched: ["MySQL", "NumPy", "Pandas"],
  missing: [
    "Python",
    "Machine Learning",
    "Django",
    "MySQL",
    "NumPy",
    "Pandas",
    "Scikit-learn",
    "LLM",
    "Prompt Engineering",
    "Git",
    "GitHub"
  ]
};

// Job data (simulating backend response)
const jobData = {
  title: "Machine Learning Engineer",
  description: "We are looking for a skilled Machine Learning Engineer to join our team and help build cutting-edge AI solutions. You will work on developing, training, and deploying machine learning models to solve real-world problems. Experience with deep learning frameworks and cloud platforms is a plus.",
  mandatory_skills: ["Python", "Machine Learning", "Django", "MySQL", "NumPy", "Pandas", "Scikit-learn"],
  optional_skills: ["LLM", "Prompt Engineering", "Git", "GitHub"],
  certification_enabled: true,
  certification_weight: 0
};

// DOM Elements
const step1 = document.getElementById('step1');
const jobDetails = document.getElementById('jobDetails');
const step2 = document.getElementById('step2');
const step3 = document.getElementById('step3');
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');
const filePreview = document.getElementById('filePreview');
const fileName = document.getElementById('fileName');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingOverlay = document.getElementById('loadingOverlay');

// Step Navigation
function updateSteps(activeStep) {
  const steps = document.querySelectorAll('.step');
  steps.forEach((step, index) => {
    const stepNum = index + 1;
    step.classList.remove('active', 'completed');
    if (stepNum < activeStep) {
      step.classList.add('completed');
    } else if (stepNum === activeStep) {
      step.classList.add('active');
    }
  });
}

function hideAllSections() {
  step1.classList.remove('active');
  jobDetails.classList.remove('active');
  step2.classList.remove('active');
  step3.classList.remove('active');
}

// Navigation Functions
function showJobDetails() {
  hideAllSections();
  jobDetails.classList.add('active');
}

function goBack() {
  hideAllSections();
  step1.classList.add('active');
}

function showUpload() {
  hideAllSections();
  step2.classList.add('active');
  updateSteps(2);
}

function backToDetails() {
  hideAllSections();
  jobDetails.classList.add('active');
  updateSteps(1);
}

function backToUpload() {
  hideAllSections();
  step2.classList.add('active');
  updateSteps(2);
  // Reset file upload
  removeFile();
}

// File Upload Handlers
uploadZone.addEventListener('click', () => {
  fileInput.click();
});

uploadZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  uploadZone.classList.add('dragover');
});

uploadZone.addEventListener('dragleave', () => {
  uploadZone.classList.remove('dragover');
});

uploadZone.addEventListener('drop', (e) => {
  e.preventDefault();
  uploadZone.classList.remove('dragover');
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    handleFile(files[0]);
  }
});

fileInput.addEventListener('change', (e) => {
  if (e.target.files.length > 0) {
    handleFile(e.target.files[0]);
  }
});

function handleFile(file) {
  // Check file type
  const allowedTypes = ['application/pdf', 'application/msword', 
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
  
  if (!allowedTypes.includes(file.type)) {
    alert('Please upload a PDF or Word document');
    return;
  }

  // Check file size (5MB)
  if (file.size > 5 * 1024 * 1024) {
    alert('File size must be less than 5MB');
    return;
  }

  fileName.textContent = file.name;
  filePreview.style.display = 'flex';
  uploadZone.style.display = 'none';
  analyzeBtn.disabled = false;
}

function removeFile() {
  fileInput.value = '';
  filePreview.style.display = 'none';
  uploadZone.style.display = 'block';
  analyzeBtn.disabled = true;
}

// Analyze Resume
function analyzeResume() {
  loadingOverlay.classList.add('active');

  const file = fileInput.files[0];

  if (!file) {
    alert("Please upload a file first");
    loadingOverlay.classList.remove('active');
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  fetch("/analyze-resume", {
    method: "POST",
    body: formData
  })
    .then(response => {
      if (!response.ok) {
        throw new Error("Server error");
      }
      return response.json();
    })
    .then(data => {
      loadingOverlay.classList.remove('active');

      // IMPORTANT: overwrite your existing variable
      Object.assign(analysisData, data);
      console.log(data)
      showAnalysis(data);
    })
    .catch(error => {
      console.error("Error:", error);
      loadingOverlay.classList.remove('active');
      alert("Something went wrong while analyzing resume.");
    });
}

function showAnalysis(data) {
  hideAllSections();
  step3.classList.add('active');
  updateSteps(3);
  updateAnalysisUI(data); // use fresh API data
}

function updateAnalysisUI(data) {
  // Update candidate name
  document.getElementById('candidateName').textContent = data.name;

  // Update match badge
  const matchBadge = document.getElementById('matchBadge');
  matchBadge.textContent = data.category;
  matchBadge.className = 'match-badge';
  if (data.final < 0.4) {
    matchBadge.classList.add('weak');
  } else if (data.final < 0.7) {
    matchBadge.classList.add('moderate');
  } else {
    matchBadge.classList.add('strong');
  }

  // Update scores
  const semanticPercent = Math.round(data.semantic * 100);
  const skillPercent = Math.round(data.skill * 100);
  const finalPercent = Math.round(data.final * 100);

  document.getElementById('semanticScore').textContent = semanticPercent + '%';
  document.getElementById('skillScore').textContent = skillPercent + '%';
  document.getElementById('finalScore').textContent = finalPercent + '%';

  // Update score bars with animation
  setTimeout(() => {
    document.querySelector('.score-fill.semantic').style.width = semanticPercent + '%';
    document.querySelector('.score-fill.skill').style.width = skillPercent + '%';
    document.querySelector('.score-fill.final').style.width = finalPercent + '%';

    // Update bar chart
    document.getElementById('semanticBar').style.width = semanticPercent + '%';
    document.getElementById('skillBar').style.width = skillPercent + '%';
    document.getElementById('finalBar').style.width = finalPercent + '%';
  }, 100);

  // Update radial chart
  document.getElementById('radialValue').textContent = finalPercent + '%';
  const circumference = 2 * Math.PI * 45;
  const progress = (finalPercent / 100) * circumference;
  document.querySelector('.radial-progress').style.strokeDasharray = `${progress} ${circumference}`;

  // Update pie chart
  const totalSkills = data.matched.length + data.missing.length;
  const matchedPercent = (data.matched.length / totalSkills) * 100;
  const missingPercent = (data.missing.length / totalSkills) * 100;
  
  const circleCircumference = 2 * Math.PI * 40;
  const matchedDash = (matchedPercent / 100) * circleCircumference;
  const missingDash = (missingPercent / 100) * circleCircumference;

  document.querySelector('.pie-matched').style.strokeDasharray = `${matchedDash} ${circleCircumference}`;
  document.querySelector('.pie-missing').style.strokeDasharray = `${missingDash} ${circleCircumference}`;
  document.querySelector('.pie-missing').style.strokeDashoffset = `-${matchedDash}`;

  document.querySelector('.pie-total').textContent = totalSkills;

  // Update legend
  document.querySelector('.pie-legend').innerHTML = `
    <div class="legend-item">
      <span class="legend-dot matched"></span>
      <span>Matched (${data.matched.length})</span>
    </div>
    <div class="legend-item">
      <span class="legend-dot missing"></span>
      <span>Missing (${data.missing.length})</span>
    </div>
  `;

  // Update skills lists
  const matchedList = document.getElementById('matchedSkillsList');
  const missingList = document.getElementById('missingSkillsList');

  matchedList.innerHTML = data.matched.map(skill => 
    `<span class="skill-tag success">${skill}</span>`
  ).join('');

  missingList.innerHTML = data.missing.map(skill => 
    `<span class="skill-tag danger">${skill}</span>`
  ).join('');
}

function renderJobs(jobs) {
  const container = document.getElementById("jobContainer");

  container.innerHTML = jobs.map(job => `
    <div class="job-card">
      <div class="job-header">
        <h2 class="job-title">${job.title}</h2>
        <span class="job-badge">Full Time</span>
      </div>

      <p class="job-description-short">
        ${job.description.substring(0, 120)}...
      </p>

      <div class="skills-preview">
        ${job.mandatory_skills.slice(0, 3).map(skill =>
          `<span class="skill-tag">${skill}</span>`
        ).join('')}
        <span class="skill-tag-more">
          +${Math.max(0, job.mandatory_skills.length - 3)} more
        </span>
      </div>

      <button class="btn btn-primary" onclick="selectJob(${job.id})">
        See More
      </button>
    </div>
    <br>
  `).join('');
}

function loadJobs() {
  console.log("Hello");
  fetch("/jobs")
    .then(res => res.json())
    .then(data => {
      jobsData = data;
      console.log(jobsData);
      renderJobs(jobsData);
    })
    .catch(err => {
      console.error("Failed to load jobs:", err);
    });
}

function selectJob(jobId) {
  selectedJobId = jobId;
  selectedJobData = jobsData.find(j => j.id === jobId);

  updateJobDetailsUI(selectedJobData);
  showJobDetails();
}

function updateJobDetailsUI(job) {
  document.getElementById("detailTitle").textContent = job.title;
  document.getElementById("detailDescription").textContent = job.description;

  // Mandatory Skills
  document.getElementById("mandatorySkills").innerHTML =
    job.mandatory_skills.map(skill =>
      `<span class="skill-tag mandatory">${skill}</span>`
    ).join('');

  // Optional Skills
  document.getElementById("optionalSkills").innerHTML =
    job.optional_skills.map(skill =>
      `<span class="skill-tag optional">${skill}</span>`
    ).join('');

  // Certification
  document.getElementById("certificationInfo").textContent =
    job.certification_enabled
      ? `Certification Enabled (Weight: ${job.certification_weight * 100}%)`
      : "No Certification Required";
}
// Initialize
document.addEventListener('DOMContentLoaded', () => {
  updateSteps(1);
  loadJobs();
});
