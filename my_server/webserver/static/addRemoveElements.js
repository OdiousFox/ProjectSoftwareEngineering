function addElement(parentName, elementType, elementId){
    var parent = document.getElementById(parentName);
    var child = document.createElement(elementType);
    child.id = elementId;
    parent.appendChild(child);
}

function removeElement(parentName){
    var parent = document.getElementById(parentName);
    var child = parent.lastChild;
    parent.removeChild(child);
}