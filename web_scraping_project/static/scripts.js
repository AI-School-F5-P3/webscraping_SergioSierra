function toggleBio(button) {
    const bioParagraph = button.parentElement.nextElementSibling.nextElementSibling;
    const authorName = button.parentElement.textContent.split('— ')[1].split(' ')[0]; // Obtener el nombre del autor
    
    // Enviar la solicitud AJAX al servidor
    fetch('/log_bio_view', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ author: authorName })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));

    // Mostrar u ocultar la biografía
    if (bioParagraph.style.display === "none") {
        bioParagraph.style.display = "block";
        button.textContent = "Ocultar Biografía";
    } else {
        bioParagraph.style.display = "none";
        button.textContent = "Ver Biografía";
    }
}
