class ArticlesController < ApplicationController
	def index
		@articles = Article.all
	end

	def new
	end

	def create
		@article = Article.new(article_params)
		if @article.save
			redirect_to @article
		else
			render 'new'
		end
		#puts @article
		# render plain: params[:article].inspect
	end

	def show
		puts params
		@article = Article.find(params[:id])
	end

	private
		def article_params
			params.require(:article).permit(:title, :Text)
		end
end
