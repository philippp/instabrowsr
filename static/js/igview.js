var igview = {};

igview.showPicture = function(data){
  var contents = $("<div></div>");
  var title = 'untitled';
  if (data.caption) {
    title = data.caption['text'];
  }
  contents.append($("<img src='"+data.user['profile_picture']+"'/>").css({
      'position':'absolute'
    }));
    contents.append($("<img src='"+data.images['standard_resolution']['url']+"'/>"));
    contents.dialog({
      'position':[100,0],
      'width':650,
      'title':title
    });
};