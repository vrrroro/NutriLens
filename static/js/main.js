

document.addEventListener('DOMContentLoaded', function () {

    const cursor = document.getElementById('custom-cursor');
    if (cursor && window.innerWidth > 768) {
        document.addEventListener('mousemove', (e) => {

            requestAnimationFrame(() => {
                cursor.style.left = e.clientX + 'px';
                cursor.style.top = e.clientY + 'px';
            });
        });

        const interactables = document.querySelectorAll('a, button, input, .card, .step-card, .insight-item');
        interactables.forEach(el => {
            el.addEventListener('mouseenter', () => cursor.classList.add('hovering'));
            el.addEventListener('mouseleave', () => cursor.classList.remove('hovering'));
        });
    }

    const canvas = document.getElementById('bg-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let width, height;
        let particles = [];
        const mouse = { x: -1000, y: -1000, radius: 150 };

        window.addEventListener('mousemove', (e) => {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        });

        window.addEventListener('mouseout', () => {
            mouse.x = -1000;
            mouse.y = -1000;
        });

        function initCanvas() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
            particles = [];

            const numParticles = Math.floor((width * height) / 9000);

            for (let i = 0; i < numParticles; i++) {
                particles.push({
                    x: Math.random() * width,
                    y: Math.random() * height,
                    vx: (Math.random() - 0.5) * 0.8,
                    vy: (Math.random() - 0.5) * 0.8,
                    size: Math.random() * 1.5 + 0.5,
                });
            }
        }

        function drawParticles() {
            ctx.clearRect(0, 0, width, height);
            ctx.fillStyle = 'rgba(0, 255, 204, 0.8)';

            for (let i = 0; i < particles.length; i++) {
                let p = particles[i];

                p.x += p.vx;
                p.y += p.vy;

                if (p.x < 0 || p.x > width) p.vx *= -1;
                if (p.y < 0 || p.y > height) p.vy *= -1;

                let dx = mouse.x - p.x;
                let dy = mouse.y - p.y;
                let distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < mouse.radius) {
                    let force = (mouse.radius - distance) / mouse.radius;
                    p.x -= dx * force * 0.03;
                    p.y -= dy * force * 0.03;
                }

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fill();

                for (let j = i + 1; j < particles.length; j++) {
                    let p2 = particles[j];
                    let ddx = p.x - p2.x;
                    let ddy = p.y - p2.y;
                    let dist = Math.sqrt(ddx * ddx + ddy * ddy);

                    if (dist < 100) {
                        ctx.beginPath();
                        ctx.strokeStyle = `rgba(0, 255, 204, ${0.15 - dist/100 * 0.15})`;
                        ctx.lineWidth = 0.5;
                        ctx.moveTo(p.x, p.y);
                        ctx.lineTo(p2.x, p2.y);
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(drawParticles);
        }

        initCanvas();
        drawParticles();
        window.addEventListener('resize', initCanvas);
    }

    const demoValues = {
        protein:    45, iron:       12, calcium:    800, vitamin_c:  70,
        magnesium:  320, zinc:       9,  vitamin_d:  15, vitamin_b12: 2.0
    };

    const demoBtn = document.getElementById('demo-fill-btn');
    if (demoBtn) {
        demoBtn.addEventListener('click', function () {
            for (const [fieldName, value] of Object.entries(demoValues)) {
                const input = document.getElementById(fieldName);
                if (input) {
                    input.value = value;
                    input.classList.remove('error');
                    const errorEl = document.getElementById('error-' + fieldName);
                    if (errorEl) errorEl.classList.remove('visible');
                }
            }

            const section = document.querySelector('.form-section');
            section.style.boxShadow = "0 0 40px rgba(0,255,204,0.3)";
            setTimeout(() => section.style.boxShadow = "none", 500);
        });
    }

    const form = document.getElementById('nutrition-form');
    if (form) {
        form.addEventListener('submit', function (event) {
            let isValid = true;
            const fields = [
                'protein', 'iron', 'calcium', 'vitamin_c',
                'magnesium', 'zinc', 'vitamin_d', 'vitamin_b12'
            ];

            fields.forEach(function (fieldName) {
                const input = document.getElementById(fieldName);
                const errorEl = document.getElementById('error-' + fieldName);
                if (!input) return;

                const value = input.value.trim();

                if (value === '' || isNaN(parseFloat(value)) || parseFloat(value) < 0) {
                    input.classList.add('error');
                    if (errorEl) errorEl.classList.add('visible');
                    isValid = false;
                } else {
                    input.classList.remove('error');
                    if (errorEl) errorEl.classList.remove('visible');
                }
            });

            if (!isValid) {
                event.preventDefault();
                const firstError = form.querySelector('.error');
                if (firstError) firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });

        const allInputs = form.querySelectorAll('input[type="number"]');
        allInputs.forEach(input => {
            input.addEventListener('input', () => {
                if (input.value.trim() !== '' && parseFloat(input.value) >= 0) {
                    input.classList.remove('error');
                    const errorEl = document.getElementById('error-' + input.id);
                    if (errorEl) errorEl.classList.remove('visible');
                }
            });
        });
    }

    const progressBars = document.querySelectorAll('.progress-bar');
    if (progressBars.length > 0) {
        setTimeout(function () {
            progressBars.forEach(function (bar) {
                const width = bar.getAttribute('data-width') || 0;
                bar.style.width = width + '%';
            });
        }, 300); 
    }

    if (typeof nutrientData !== 'undefined' && nutrientData.length > 0) {
        Chart.defaults.color = '#94a3b8';
        Chart.defaults.font.family = "'Orbitron', sans-serif";

        const labels       = nutrientData.map(d => d.name);
        const intakeValues = nutrientData.map(d => d.intake);
        const rdaValues    = nutrientData.map(d => d.rda);
        const probabilities = nutrientData.map(d => d.probability);

        const riskColors   = nutrientData.map(d => d.risk_color);

        const barCanvas = document.getElementById('barChart');
        if (barCanvas) {
            new Chart(barCanvas, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Your Intake',
                            data: intakeValues,
                            backgroundColor: 'rgba(0, 255, 204, 0.7)',
                            borderColor: '#00ffcc',
                            borderWidth: 2,
                            borderRadius: 4
                        },
                        {
                            label: 'RDA Requirement',
                            data: rdaValues,
                            backgroundColor: 'rgba(56, 189, 248, 0.3)',
                            borderColor: '#38bdf8',
                            borderWidth: 2,
                            borderRadius: 4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: { labels: { color: '#e0f2fe' } },
                        tooltip: {
                            backgroundColor: 'rgba(10, 15, 25, 0.9)',
                            titleColor: '#00ffcc',
                            bodyColor: '#e0f2fe',
                            borderColor: '#00ffcc',
                            borderWidth: 1,
                            titleFont: { family: "'Orbitron'" },
                            bodyFont: { family: "'Inter'" }
                        }
                    },
                    scales: {
                        x: {
                            ticks: { color: '#94a3b8', font: { size: 10 } },
                            grid:  { color: 'rgba(0, 255, 204, 0.1)' }
                        },
                        y: {
                            ticks: { color: '#94a3b8' },
                            grid:  { color: 'rgba(0, 255, 204, 0.1)' },
                            beginAtZero: true
                        }
                    },
                    animation: { duration: 1200, easing: 'easeOutQuart' }
                }
            });
        }

        const radarCanvas = document.getElementById('radarChart');
        if (radarCanvas) {
            new Chart(radarCanvas, {
                type: 'radar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Deficiency Probability (%)',
                        data: probabilities,
                        backgroundColor: 'rgba(244, 63, 94, 0.15)', 
                        borderColor: '#f43f5e',
                        borderWidth: 3,
                        pointBackgroundColor: riskColors,
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 6,
                        pointHoverRadius: 10
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: { labels: { color: '#e0f2fe' } },
                        tooltip: {
                            backgroundColor: 'rgba(10, 15, 25, 0.9)',
                            titleColor: '#f43f5e',
                            bodyColor: '#e0f2fe',
                            borderColor: '#f43f5e',
                            borderWidth: 1,
                            callbacks: {
                                label: function(ctx) { return ctx.parsed.r + '% deficiency probability'; }
                            }
                        }
                    },
                    scales: {
                        r: {
                            beginAtZero: true,
                            max: 100,
                            ticks: {
                                color: '#94a3b8',
                                backdropColor: 'transparent',
                                stepSize: 20
                            },
                            grid: { color: 'rgba(244, 63, 94, 0.2)' },
                            angleLines: { color: 'rgba(244, 63, 94, 0.2)' },
                            pointLabels: {
                                color: '#e0f2fe',
                                font: { size: 10, family: "'Inter'" }
                            }
                        }
                    },
                    animation: { duration: 1500, easing: 'easeOutQuart' }
                }
            });
        }
    }
});
