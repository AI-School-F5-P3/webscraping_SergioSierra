function toggleBio(button) {
    const bioParagraph = button.parentElement.nextElementSibling.nextElementSibling;
    if (bioParagraph.style.display === "none") {
        bioParagraph.style.display = "block";
        button.textContent = "Ocultar Biografía";
    } else {
        bioParagraph.style.display = "none";
        button.textContent = "Ver Biografía";
    }
}
