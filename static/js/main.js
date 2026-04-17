document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("bg-canvas");
    const ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = [];
    for (let i = 0; i < 100; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 2 + 0.5,
            speedX: Math.random() * 0.5 - 0.25,
            speedY: Math.random() * 0.5 - 0.25,
            opacity: Math.random() * 0.5 + 0.1
        });
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach(p => {
            p.x += p.speedX;
            p.y += p.speedY;

            if (p.x < 0) p.x = canvas.width;
            if (p.x > canvas.width) p.x = 0;
            if (p.y < 0) p.y = canvas.height;
            if (p.y > canvas.height) p.y = 0;

            ctx.fillStyle = `rgba(0, 255, 204, ${p.opacity})`;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
        });
        requestAnimationFrame(animate);
    }
    animate();

    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });

    const cursor = document.getElementById('custom-cursor');
    if (cursor) {
        document.addEventListener('mousemove', (e) => {
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
        });

        const interactables = document.querySelectorAll('a, button, input, select');
        interactables.forEach(el => {
            el.addEventListener('mouseenter', () => cursor.classList.add('hovering'));
            el.addEventListener('mouseleave', () => cursor.classList.remove('hovering'));
        });
    }

    let state = {
        gender: "Female",
        foods: [],
        currentMeal: null,
        currentFood: null,
    };

    const stepGender = document.getElementById('step-gender');
    const stepTracker = document.getElementById('step-tracker');
    const genderBadge = document.getElementById('current-gender-badge');
    const foodsListElem = document.getElementById('foods-list');

    const tpSelection = document.getElementById('meal-type-selection');
    const foodSelection = document.getElementById('food-selection');
    const quantSelection = document.getElementById('quantity-input');

    const btnAddMeal = document.getElementById('btn-add-meal');
    const btnDemoFill = document.getElementById('btn-demo-fill');
    const btnSubmitAnalysis = document.getElementById('btn-submit-analysis');
    const btnConfirmFood = document.getElementById('btn-confirm-food');
    const btnCancelFood = document.getElementById('btn-cancel-food');

    document.querySelectorAll('.gender-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            state.gender = e.target.getAttribute('data-gender');
            genderBadge.textContent = state.gender === "Male" ? "👨 Male Profile" : "👩 Female Profile";
            stepGender.classList.remove('active-step');
            stepGender.classList.add('hidden-step');
            stepTracker.classList.remove('hidden-step');
            stepTracker.classList.add('active-step');
        });
    });

    if (btnAddMeal) {
        btnAddMeal.addEventListener('click', () => {
            tpSelection.classList.remove('hidden');
            foodSelection.classList.add('hidden');
            quantSelection.classList.add('hidden');
            btnAddMeal.style.display = 'none';
        });
    }

    if (btnDemoFill) {
        btnDemoFill.addEventListener('click', () => {
            state.foods = [
                { meal: "Breakfast", name: "Dosa", weight: 200, unit: "g" },
                { meal: "Breakfast", name: "Milk", weight: 300, unit: "ml" },
                { meal: "Lunch", name: "Rice", weight: 200, unit: "g" },
                { meal: "Lunch", name: "Dal", weight: 150, unit: "g" },
                { meal: "Lunch", name: "Sabzi", weight: 200, unit: "g" },
                { meal: "Snacks", name: "Egg", weight: 100, unit: "g" },
                { meal: "Dinner", name: "Roti", weight: 150, unit: "g" },
                { meal: "Dinner", name: "Paneer", weight: 200, unit: "g" }
            ];
            renderFoodsList();
            btnSubmitAnalysis.style.display = 'inline-block';
            updatePayload();
        });
    }

    document.querySelectorAll('.meal-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            state.currentMeal = e.target.getAttribute('data-meal');
            document.getElementById('selected-meal-label').textContent = state.currentMeal;
            tpSelection.classList.add('hidden');
            foodSelection.classList.remove('hidden');
        });
    });

    document.querySelectorAll('.food-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            state.currentFood = e.target.getAttribute('data-food');
            document.getElementById('selected-food-label').textContent = state.currentFood;
            foodSelection.classList.add('hidden');
            quantSelection.classList.remove('hidden');
            document.getElementById('food-quantity').value = '';
        });
    });

    if (btnConfirmFood) {
        btnConfirmFood.addEventListener('click', () => {
            const qty = parseFloat(document.getElementById('food-quantity').value);
            const unit = document.getElementById('food-unit').value;

            if (!qty || qty <= 0) {
                alert("Please enter a valid quantity.");
                return;
            }

            state.foods.push({
                meal: state.currentMeal,
                name: state.currentFood,
                weight: qty,
                unit: unit
            });

            renderFoodsList();

            quantSelection.classList.add('hidden');
            btnAddMeal.style.display = 'inline-block';
            btnSubmitAnalysis.style.display = 'inline-block';
            updatePayload();
        });
    }

    if (btnCancelFood) {
        btnCancelFood.addEventListener('click', () => {
            quantSelection.classList.add('hidden');
            foodSelection.classList.add('hidden');
            tpSelection.classList.add('hidden');
            btnAddMeal.style.display = 'inline-block';
        });
    }

    function renderFoodsList() {
        foodsListElem.innerHTML = '';
        state.foods.forEach((item, index) => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span><strong>${item.name}</strong> (${item.meal})</span>
                <span>${item.weight}${item.unit} <button type="button" class="btn btn-ghost remove-food-btn" data-idx="${index}" style="padding:4px 8px; font-size:0.8rem; margin-left:10px;">❌</button></span>
            `;
            foodsListElem.appendChild(li);
        });

        document.querySelectorAll('.remove-food-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const idx = parseInt(e.target.getAttribute('data-idx'));
                state.foods.splice(idx, 1);
                renderFoodsList();
                updatePayload();
                if (state.foods.length === 0) {
                    btnSubmitAnalysis.style.display = 'none';
                }
            });
        });
    }

    function updatePayload() {
        const payloadInput = document.getElementById('payload');
        if (payloadInput) {
            payloadInput.value = JSON.stringify(state);
        }
    }


    if (typeof nutrientData !== 'undefined' && nutrientData.length > 0) {
        const labels = nutrientData.map(d => d.name);

        const intakePctData = nutrientData.map(d => d.intake_pct);
        const bgColors = nutrientData.map(d => d.risk_color);

        const ctxBar = document.getElementById('barChart');
        if (ctxBar) {
            new Chart(ctxBar, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: '% of RDA Reached',
                        data: intakePctData,
                        backgroundColor: bgColors,
                        borderWidth: 1,
                        borderColor: 'rgba(255,255,255,0.1)'
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            ticks: { color: '#94a3b8' },
                            grid: { color: 'rgba(255,255,255,0.05)' }
                        },
                        x: {
                            ticks: { color: '#e0f2fe', font: { family: 'Orbitron', size: 10 } },
                            grid: { display: false }
                        }
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: 'rgba(10,15,25,0.9)',
                            titleFont: { family: 'Orbitron' },
                            callbacks: {
                                label: function (context) {
                                    return context.parsed.y + '% of Target RDA';
                                }
                            }
                        }
                    }
                }
            });
        }

        const probData = nutrientData.map(d => d.probability);

        const ctxRadar = document.getElementById('radarChart');
        if (ctxRadar) {
            new Chart(ctxRadar, {
                type: 'radar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Deficiency Risk (%)',
                        data: probData,
                        backgroundColor: 'rgba(244, 63, 94, 0.2)',
                        borderColor: '#f43f5e',
                        pointBackgroundColor: '#f43f5e',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: '#f43f5e',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        r: {
                            angleLines: { color: 'rgba(255,255,255,0.1)' },
                            grid: { color: 'rgba(255,255,255,0.05)' },
                            pointLabels: { color: '#00ffcc', font: { family: 'Orbitron', size: 10 } },
                            ticks: { display: false, min: 0, max: 100 }
                        }
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: 'rgba(10,15,25,0.9)',
                            titleFont: { family: 'Orbitron' },
                            callbacks: {
                                label: function (context) {
                                    return context.parsed.r + '% Risk';
                                }
                            }
                        }
                    }
                }
            });
        }
    }
});
