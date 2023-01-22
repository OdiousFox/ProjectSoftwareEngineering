function getDropDownOption(selectedID) {
  var obj = document.getElementById(selectedID);
  return obj.options[obj.selectedIndex].text;
}

function getMultipleDropDownOption(selectedID){
var selection = document.getElementById(selectedID);
const selectedValues = [].filter
    .call(selection.options, option=> option.selected)
    .map(option => option.text)
return selectedValues
}

function getSliderOption(selectedID){
  var selection = document.getElementById(selectedID);
  return selection.value;
}