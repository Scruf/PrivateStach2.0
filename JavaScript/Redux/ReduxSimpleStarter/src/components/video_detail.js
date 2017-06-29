import React from 'react'

const VideoDetail = ({video})=>{

	if (!video){
		return (
				<div> Loading ... </div>
			)
	}
	const video_id = video.id.videoId;
	const url = `https://www.youtube.com/embed/${video_id}`
	return (
		<div className="video-detail col-md-8">
			<div className="embed-reponsive embed-reponsive-16by9">
				<iframe className="embed-reponsive-item" src={url}>

				</iframe>
			</div>
			<div className="details">
				<div>{video.snippet.title}</div>
				<div>{video.snippet.description}</div>
			</div>
		</div>
	)
}
export default VideoDetail