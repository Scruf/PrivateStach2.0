import React from 'react';
import ReactDOM from 'react-dom';

//Creating new component and this component will produce some html
const App = function(){
  return <div> Hi </div>;
}

//Take this component and put it on the page
ReactDOM.render(<App />, document.querySelector('.container'));
