function updateProductVariation(variationId, type) {
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch(`/api/update_variation/${variationId}/`, {  // Update this URL to your actual API endpoint
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
        .then(response => response.json())
        .then(data => {

            document.querySelector('.container-product-details').innerHTML = data.html;
        })
        .catch(error => console.error('Error updating product variations:', error));
}



