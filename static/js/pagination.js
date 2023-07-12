window.addEventListener('DOMContentLoaded', (event) => {
    const buttonContainer = document.getElementById('buttonContainer');


    const buttonCount = 5;
    const buttonSize = 30;

    let currentPage = 1;
    let totalPages = buttonCount / 4;

    function renderButton() {

        buttonContainer.innerHTML = '';
        if (currentPage > 1) {
            const prevButton = createButton('...');
            prevButton.addEventListener('click', () => {
                currentPage--;
                renderButton();
            });
            buttonContainer.appendChild(prevButton);
        }


        const startButton = (currentPage - 1) * 4;
        let endButton = startButton + 4;

        if (endButton > buttonCount) {
            endButton = buttonCount;
        }


        for (let i = startButton; i < endButton; i++) {
            const button = createButton(i + 1);
            buttonContainer.appendChild(button);
        }


        if (currentPage < totalPages) {
            const nextButton = createButton('…');
            nextButton.addEventListener('click', () => {
                currentPage++;
                renderButton();
            });
            buttonContainer.appendChild(nextButton);
        }
    }


    function createButton(number) {
        //onclick() onclick에 1 강제로 누르기 
        const button = document.createElement('div');
        button.classList.add('button');
        button.id = number;
        button.style.width = buttonSize + 'px';
        button.style.height = buttonSize + 'px';
        button.innerText = number;
        return button;
    }


    renderButton();
});
