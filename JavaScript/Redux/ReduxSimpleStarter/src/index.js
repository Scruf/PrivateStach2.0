import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import SearchBar from './components/search_bar';
import VideoList from './components/video_list';
import YTSearch from 'youtube-api-search'
const API_KEY = 'AIzaSyB1Pf2gYt9IdprDA9cLWx3rDuhkxheJAe8'

//Creating new component and this component will produce some html
class App extends Component{
  constructor(props){
  	super(props);
  	this.state  = {videos:[]}
  	
	YTSearch({key:API_KEY,term:'Cats'},(videos)=>{
		this.setState({videos})
	})
  }

  render(){
	  return (<div> <SearchBar />
	  				<VideoList videos={this.state.videos}/>
			 </div>)
  	
  }
}


//Take this component and put it on the page
ReactDOM.render(<App />, document.querySelector('.container'));
