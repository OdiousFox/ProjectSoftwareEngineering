function addElementToParent(parent, elementType, classType, elementId){
    var child = document.createElement(elementType);
    child.classList.add(classType);
    child.id = elementId;
    parent.appendChild(child);
    return child;
}

function addRemoveButton(parent){
    const button = document.createElement('button');
    button.innerHTML = 'Remove';
    button.addEventListener('click', function() {
        parent.remove();
    });
    parent.appendChild(button);
}