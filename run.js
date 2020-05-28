
function foo() {

  var x = [
    "foo",
    "bar",
    "baz",
    "bash",
  ]

  for (var i = 0; i < x.length; i++) {
    console.log(handleSwitch(x[i]))
  }

  function handleSwitch(word) {
    let response = null

    switch (word) {

      
      case "foo":
        response = "foo waaahaawaaaahaaa"
        break;

      case "bar":
        response = "bar waaahaawaaaahaaa"
        break;

      case "baz":
        response = "baz waaahaawaaaahaaa"
        break;

      case "bash":
        response = "bash waaahaawaaaahaaa"
        break;


    }

    return response;
  }
};


foo()