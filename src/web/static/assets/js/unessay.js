document.getElementById('recommendationForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var keywords = document.getElementById('keywords').value;
    fetchRecommendations(keywords);
});

function fetchRecommendations(keywords) {
    fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ keywords: keywords })
    })
    .then(response => response.json())
    .then(data => displayRecommendations(data));
}

function displayRecommendations(data) {
    var recommendationsContainer = document.getElementById('recommendations');
    recommendationsContainer.innerHTML = '';

    if (data && data.length > 0) {
        data.forEach(recipe => {
            var recipeElement = document.createElement('div');
            recipeElement.innerHTML = `
                <h3>${recipe.name}</h3>
                <img src="${recipe.image}" alt="${recipe.name}">
                <a href="${recipe.link}" target="_blank">View Recipe</a>
            `;
            recommendationsContainer.appendChild(recipeElement);
        });
    } else {
        recommendationsContainer.innerHTML = '<p>No recommendations found. Please try different words.</p>';
    }
}

