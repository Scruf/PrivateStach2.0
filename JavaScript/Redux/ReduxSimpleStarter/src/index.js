import React from 'react';
import ReactDOM from 'react-dom';
import SearchBar from './components/search_bar';

const API_KEY = 'AIzaSyB1Pf2gYt9IdprDA9cLWx3rDuhkxheJAe8'
//Creating new component and this component will produce some html
const App = () => {
  return (<div> <SearchBar />
  		 </div>)
}

//Take this component and put it on the page
ReactDOM.render(<App />, document.querySelector('.container'));
