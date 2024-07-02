// displays image on input and adds new input
let n = 1

function addImageToImageInputs(imgSrc) {
    const container = document.getElementById('columns');
    const index = (n++).toString();

    const inputDiv = container.lastElementChild
    const clonedInput = inputDiv.cloneNode(true);
    $(clonedInput).attr('id', 'col' + index)
    $(clonedInput).find('input').attr('id', 'addImage' + index)
    $(clonedInput).find('label').attr('for', 'addImage' + index)
    $(clonedInput).find('label').css('cursor', 'pointer')
    $(clonedInput).find('input').val('')
    $(clonedInput).find('input').on('input', function onImageInput() {
        if (this.files && this.files[0]) {
            const imgSourceBlob = URL.createObjectURL(this.files[0]);   // set src to blob url
            addImageToImageInputs(imgSourceBlob);
        }
    })
    $(inputDiv).find('label').css('display', 'none');
    $(inputDiv).find('input').css('display', 'none')
    $(inputDiv).addClass('imagesCentered')
    // create displayed image for input
    const ribbonDiv = document.createElement('div');
    const ribbonDivIcon = document.createElement('i');
    const imgDiv = document.createElement('div');
    const img = document.createElement('img')

    img.style.maxHeight = '180px'
    if (imgSrc) {
        img.src = imgSrc
    }
    ribbonDiv.className = 'ui grey right ribbon icon label'
    ribbonDivIcon.className = 'delete icon'
    imgDiv.className = 'ui image'
    imgDiv.name = 'imgDiv'

    ribbonDiv.appendChild(ribbonDivIcon)
    imgDiv.appendChild(ribbonDiv)
    imgDiv.appendChild(img)

    $(inputDiv).append(imgDiv);


    // Append the new div to an existing div with id "container"

    container.appendChild(clonedInput)
    $('#imgValidate').val(container.childElementCount)

    if (container.childElementCount > 8) {
        clonedInput.style.display = 'none'
    }


    ribbonDivIcon.onclick = function () {
        const img = this.parentElement.nextElementSibling
        URL.revokeObjectURL(img.src)
        this.parentElement.parentElement.parentElement.remove();
        console.log(container.childElementCount)
        if (container.childElementCount <= 8) {
            clonedInput.style.display = 'block'
        }
        if (container.childElementCount === 1) {
            $('#imgValidate').val('0')
        }
    }
}


// delete messages on icon click
document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
        const $notification = $delete.parentNode;
        $delete.addEventListener('click', () => {
            $notification.parentNode.removeChild($notification);
        });
    });
});

// handle images - load and display
const fileInputs = document.getElementsByName('file')
fileInputs.forEach(function (fileInput) {
    fileInput.addEventListener('input', function onImageInput() {
        if (this.files && this.files[0]) {
            const imgSourceBlob = URL.createObjectURL(this.files[0]);   // set src to blob url
            addImageToImageInputs(imgSourceBlob);
        }
    })
})

const ingredientField = document.getElementById('ingRow3')
const clonedInput = ingredientField.cloneNode(true);
let nn = 3

function addFieldToIngredients() {
    const clonedClone = clonedInput.cloneNode(true)

    const idIndex = (nn += 1).toString()
    $(clonedClone).attr('id', 'ingRow' + idIndex)
    const ingContainer = document.getElementById('ingredientsField');
    ingContainer.appendChild(clonedClone);

}
let nID = 1
function addFieldToSteps() {
    const firstStepField = document.getElementById('firstStepField')
    const clonedStepField = firstStepField.cloneNode(true);
    $(clonedStepField).find('label').remove()
    $(clonedStepField).find('textarea').addClass('txtArea')
    $(clonedStepField).attr('id', 'stepField' + (nID += 1).toString())

    const icon = document.createElement('i');
    const button = document.createElement('button');
    const popUp = document.createElement('div');
    const stepsContainer = document.getElementById('stepsField');
    const nextN = (stepsContainer.childElementCount).toString()
    icon.className = 'large close icon';
    button.className = 'ui icon basic button';
    button.type = 'button';
    button.onclick = function () {
        $(this).closest('.fields').remove();
    };
    popUp.className = 'ui flowing popup transition hidden';
    button.appendChild(icon);
    popUp.appendChild(button);
    $(clonedStepField).find('textarea').val(nextN + '. ')
    $(clonedStepField).find(".input").append($(popUp))
    stepsContainer.appendChild(clonedStepField);
    $(".txtArea").popup({on: 'focus', position: 'right center'});
}
