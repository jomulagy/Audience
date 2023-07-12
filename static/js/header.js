let vh = window.innerHeight * 0.01;
document.documentElement.style.setProperty('--vh', vh + 'px');
window.addEventListener('resize', () => {
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', vh + 'px');
});

document.addEventListener('DOMContentLoaded', () => {
	var scrollable = new scrollEvent();
});

scrollEvent = function(){
	var _this = this;
	this.els = {
		scrollHead : document.querySelector('.scroll-head'),
	}
	this.position = {
		scrollTop : 0,
		scrollLeft : 0,
		scrollLast : 0,
		direction : 'down',
	}
	// scroll position  
	this.getposition = () => {
		this.position.scrollLast = this.position.scrollTop;
		this.position.scrollTop = window.scrollY;
		this.position.scrollLeft = window.scrollX;
		this.position.direction = this.getDirection();
	}
	// scroll direction 
	this.getDirection = () => {
		if(this.position.scrollLast >= this.position.scrollTop){
			return 'up';
		} else {
			return 'down';
		}
	}
	// direction class
	this.directionClass = (target) => {
		if(this.position.direction === 'down'){
			target.classList.add('scrollDown');
			target.classList.remove('scrollUp');
		} else if(this.position.direction === 'up'){
			target.classList.add('scrollUp');
			target.classList.remove('scrollDown');
		}
	}
	this.scrolloffset = (target) => {
		return window.pageYOffset + target.getBoundingClientRect().top;
	}
	this.scrollDirection = (target, margin) => { 
		var offset = parseInt(this.scrolloffset(target).toFixed(0)); 
		if( offset+target.clientHeight <= this.position.scrollTop){ 
			this.directionClass(target);
		} else if(offset < this.position.scrollTop){
			target.classList.add('fixed-header');
		} else {
			target.classList.remove('scrollUp', 'scrollDown', 'fixed-header');
		}
	}
	// scrolling define
	this.scrolling = (e) => {
		this.getposition();
		this.scrollDirection(this.els.scrollHead, 0);
	}
	this.init = () => {
		this.scrolling();
	}
	this.ready = () => {
		window.addEventListener('scroll', (e) => {
			_this.scrolling();
		});
		window.addEventListener('resize', (e) => {
			_this.init();
		});
	}
	this.ready();
}



// //keyword input
// function printName() {
// 	var keyword = document.getElementById("keyword-input").value;
// 	console.log(keyword);
//   }

// // onclick() + url
// document.addEventListener("DOMContentLoaded", function() {

// 	document.getElementById("search-button").onclick = function() {
// 		var keyword = document.getElementById("keyword-input").value;
// 		var url = `http://127.0.0.1:8000/audience/search/keyword/${encodeURIComponent(keyword)}/all/all/all/all/`;
// 		calculateTotalPagesAndGoToFirstPage(url);
//   	};
// });

  
//버튼에 url 추가하기 
