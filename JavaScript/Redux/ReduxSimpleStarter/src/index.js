import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import SearchBar from './components/search_bar';
import VideoList from './components/video_list';
import VideoDetail from './components/video_detail'
import _ from 'lodash'
import YTSearch from 'youtube-api-search'
const API_KEY = 'AIzaSyB1Pf2gYt9IdprDA9cLWx3rDuhkxheJAe8'

//Creating new component and this component will produce some html
class App extends Component{
  constructor(props){
  	super(props);
  	this.state  = { 
  		videos: [],
  		selectedVideo: null
  	}
  	this.video_search('cars')
 }
  	video_search(term){
		YTSearch({key:API_KEY,term:term},(videos)=>{
			this.setState({
					videos:videos,
					selectedVideo:videos[0]
				})
			})
 		
  	}

  render(){

  	const video_search = _.debounce((term)=>{this.video_search(term)}, 300)

  	 return (<div> 
	  				<SearchBar onSearchTermChange={video_search}/>
	  				<VideoDetail video={this.state.selectedVideo}/>
	  				<VideoList 
	  					onVideoSelect={selectedVideo => this.setState({selectedVideo})}
	  					videos={this.state.videos}/>
			 </div>)
  	
  }
}


//Take this component and put it on the page
ReactDOM.render(<App />, document.querySelector('.container'));
