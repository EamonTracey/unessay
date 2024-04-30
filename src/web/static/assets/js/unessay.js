document.getElementById('recommendationForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var keywords = document.getElementById('keywords').value;
    var numRecipes = document.getElementById('numRecipes').value;
    fetchRecommendations(keywords, numRecipes);
});

function fetchRecommendations(keywords, numRecipes) {
    fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ keywords: keywords, numRecipes: numRecipes })
    })
    .then(response => response.json())
    .then(data => displayRecommendations(data));
}

// Function to display recommendations on the page
function displayRecommendations(data) {
    var recommendationsContainer = document.getElementById('recommendations');
    recommendationsContainer.innerHTML = ''; // Clear previous recommendations

    if (data && data.length > 0) {
        data.forEach(recipe => {
            var recipeElement = document.createElement('div');
            recipeElement.classList.add('recipe'); // Add 'recipe' class

            // Create link around the image
            var link = document.createElement('a');
            link.href = recipe.link;
            link.target = '_blank'; // Open link in new tab
            // Create image element
            var image = document.createElement('img');
            image.src = recipe.image;
            image.alt = recipe.name;
            // Append image to link
            link.appendChild(image);
            // Append link to recipe element
            recipeElement.appendChild(link);

            // Create text overlay for "Go to recipe"
            var goToRecipeText = document.createElement('div');
            goToRecipeText.classList.add('go-to-recipe');
            goToRecipeText.textContent = 'Go to recipe';
            // Append text overlay to recipe element
            recipeElement.appendChild(goToRecipeText);

            // Create heading for recipe name
            var heading = document.createElement('h3');
            heading.textContent = recipe.name;
            // Append heading to recipe element
            recipeElement.appendChild(heading);

            // Append recipe element to recommendations container
            recommendationsContainer.appendChild(recipeElement);
        });
    } else {
        recommendationsContainer.innerHTML = '<p>No recipes found. Please try different search words.</p>';
    }
}

