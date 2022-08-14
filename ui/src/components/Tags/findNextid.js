export const findNextID = function (data) {
  var ids = [];
  var nextId;
  data.forEach((element) => {
    ids.push(element.id);
  });
  for (let index = 0; index < ids.length; index++) {
    if (ids.includes(String(index)) == false) {
      nextId = index;
      break;
    }
  }
  if (nextId == "") {
    nextId = ids.length;
  }
};
