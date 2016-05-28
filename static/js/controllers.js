var photokControllers = angular.module('photokControllers', [
	'photokServices'
]);

/**
*	Header controller
* -----------------
* Only here to update the navbar
*/
photokControllers.controller('HeaderController', ['$scope', '$location',
function($scope, $location) {
	$scope.isActive = function (viewLocation) {
			return viewLocation === $location.path();
	};
}]);


/**
*	Contest list controller
* -----------------------
* Only get the list with a HTTP GET query on the api
* Choose a default order
*/
photokControllers.controller('ContestListController', ['$http', '$scope', 'Contest',
function($http, $scope, Contest) {

	$http.get('api/contests').success(function(result) {
		$scope.contests = result;
			angular.forEach(result, function(value, key) {
				var date = moment(value.endDate);
				var now = moment();
				value.past = (now > date);

				value.endDate = moment(value.endDate).format('DD MMM YYYY');
			});
	});

	$scope.orderProp = 'endDate';
}]);


/**
*	Contest controller (details)
* ----------------------------
* Get the data for a specific contest (id given in the route)
* Get the images sent for a contest
* Connect with the API for sending an image for the contest
*/
photokControllers.controller('ContestDetailController', ['$http', '$scope', '$routeParams', 'Contest', 'ContestImages','ImageParticipation',
function($http, $scope, $routeParams, Contest, ContestImages, ImageParticipation) {

	$scope.participate = false;
	var contest = $routeParams.contestId;

	$scope.displayPopUp = function(){
		$scope.participate = true;
	}

	// Get the data for the contest
	$http.get('api/contests/' + contest).success(function(result) {
		$scope.contest = result;
		var date = moment(result.endDate);
		var now = moment();
		result.past = (now > date);
		result.duration = date - moment(result.startDate);
		result.span = moment(date).fromNow(true); //date - now;

		result.startDate = moment(result.startDate).format('DD MMM YYYY');
		result.endDate = moment(result.endDate).format('DD MMM YYYY');
		result.createdDate = moment(result.createdDate).format('DD MMM YYYY');
	});

	// Get the images for the contest
	// store them in an array so that we can use .push() after the form is sent
	$scope.participations = [];
	$scope.winners = {};

	$http.get('api/images/contest/' + contest).success(function(result) {
			angular.forEach(result, function(value, key) {
				var c = angular.copy(value);
				$scope.participations.push(c);

				if (c.prize == 1) $scope.winners.first = c;
				if (c.prize == 2) $scope.winners.second = c;
				if (c.prize == 3) $scope.winners.third = c;
				$scope.hidewinners = angular.equals($scope.winners,{});

			});
	});

	// Form for participation
	$scope.master = {};

	$scope.update = function(participation) {
		$scope.master = angular.copy(participation);
	};

	$scope.reset = function(form) {
		if (form) {
			form.$setPristine();
			form.$setUntouched();
		}
		$scope.participation = angular.copy($scope.master);
	};

	$scope.reset();
	// ! form

	$scope.add = function(t,i,e,c,u){
		$scope.participations.push({
			id: "?", // TODO : could this be a problem?
			title: t,
			uploadedOn: "Right now!",
			userId: u,
			exifData: e,
			path: i
		});
	}

	// Function called when form is sent
	$scope.sendImage = function () {

		alert("SENDING: "+$scope.participation.title+" for contest #"+$routeParams.contestId);
		//alert("got image: "+$scope.participation.image);

    // generate a token functions
    var rand = function() {
        return Math.random().toString(36).substr(2); // remove `0.`
    };

    var token = function() {
        return rand();
    };

    // Call the service function that will connect with the API
    ImageParticipation.sendImage($scope.participation.title, "static/images/"+token(), "exif-fake-data",contest,"1")
      // handle success
      .then(function () {
				alert('Success');
      })
      // handle error
      .catch(function () {
        //$scope.error = true;
        alert('Error');
      });

			// Add the image to the view
			// TODO: maybe try to get the *id* from the call above
			$scope.add($scope.participation.title, "static/images/"+token(), "exif-fake-data",contest,"1");
			$scope.participate = false;
  };

}]);


/**
*	Edit contest
* ----------------------------
* ...
*/
photokControllers.controller('EditContestController', ['$http', '$scope', '$routeParams', '$window', 'Contest', 'ContestImages','ImageParticipation',
function($http, $scope, $routeParams, $window, Contest, ContestImages, ImageParticipation) {

	var contestId = $routeParams.contestId;

	// Get the data for the contest
	$http.get('api/contests/' + contestId).success(function(result) {
		//console.log("result.endDate: "+result.endDate);
		//console.log("result.endDate (moment): "+moment(result.endDate).format('MM'));

		// TODO hack: month - 1 because Date moves the date by one month...
		// for some reason

		result.endDate = new Date(
			moment(result.endDate).format('YYYY'),
			moment(result.endDate).format('MM')-1,
			moment(result.endDate).format('DD'));

		result.startDate = new Date(
			moment(result.startDate).format('YYYY'),
			moment(result.startDate).format('MM')-1,
			moment(result.startDate).format('DD'));

		//console.log("result.endDate: "+result.endDate);
		//console.log("result.endDate (moment): "+moment(result.endDate).format('MM'));

		$scope.contest = result;

		//console.log("$scope.contest.endDate: "+moment($scope.contest.endDate).format('YYYY-MM-DD'));

	});

	// Get the images for the contest
	// store them in an array so that we can use .push() after the form is sent
	$scope.participations = [];
	$http.get('api/images/contest/' + contestId).success(function(result) {
			angular.forEach(result, function(value, key) {
				$scope.participations.push(value);
			});
	});

	// Function called when form is sent
	$scope.editContest = function () {

		alert("EDITING: "+$scope.contest.workingTitle);

		// Call the service function that will connect with the API
		// TODO: Add more parameters (: replace fake data in the service)
		Contest.editContest($scope.contest.id,$scope.contest.headline, $scope.contest.theme,
		$scope.contest.workingTitle, $scope.contest.description,
		moment($scope.contest.startDate).format('YYYY-MM-DD HH:mm:ss.SSS'),
		moment($scope.contest.endDate).format('YYYY-MM-DD HH:mm:ss.SSS'))
			// handle success
			.then(function () {
				alert('CONTROLLER: Success');
			})
			// handle error
			.catch(function () {
				//$scope.error = true;
				alert('CONTROLLER: Error');
			});

			alert("EDITING: Done");
	};

	// Function called when delete button is clicked
	$scope.deleteContest = function () {

		alert("DELETING: "+$scope.contest.headline+"; id : "+$scope.contest.id);

		// Call the service function that will connect with the API
		// TODO: Add more parameters (: replace fake data in the service)
		Contest.deleteContest($scope.contest.id)
			// handle success
			.then(function () {
				alert('CONTROLLER: Success');
			})
			// handle error
			.catch(function () {
				//$scope.error = true;
				alert('CONTROLLER: Error');
			});

			alert("DELETING: Done");
			$window.location.href = '/contests';

	};

}]);


/**
*	Create contest controller
* -------------------------
* Get the data for a specific contest (id given in the route)
* Get the images sent for a contest
* Connect with the API for sending an image for the contest
*/
photokControllers.controller('CreateContestController', ['$scope', '$routeParams', 'Contest', 'ContestImages',
function($scope, $routeParams, Contest, ContestImages) {
	$scope.master = {};

  $scope.update = function(contest) {
    $scope.master = angular.copy(contest);
  };

  $scope.reset = function(form) {
    if (form) {
      form.$setPristine();
      form.$setUntouched();
    }
    $scope.contest = angular.copy($scope.master);
  };

  $scope.reset();

	// Function called when form is sent
	$scope.createContest = function () {

		alert("SENDING: "+$scope.contest.headline);

		// Call the service function that will connect with the API
		// TODO: Add more parameters (: replace fake data in the service)
		Contest.createContest($scope.contest.headline, $scope.contest.workingtitle)
			// handle success
			.then(function () {
				alert('CONTROLLER: Success');
			})
			// handle error
			.catch(function () {
				//$scope.error = true;
				alert('CONTROLLER: Error');
			});

			alert("SENDING: Done");

	};

}]);


/**
*	Vote for contest
* -------------------------
* ...
*/
photokControllers.controller('VoteContestController', ['$http', '$scope', '$routeParams', '$window', 'Contest', 'ContestImages','ImageParticipation',
function($http, $scope, $routeParams, $window, Contest, ContestImages, ImageParticipation) {

	$scope.results = {first: 0, second: 0, third: 0};

	var contest = $routeParams.contestId;

	// Get the data for the contest
	$http.get('api/contests/' + contest).success(function(result) {
  	$scope.contest = result;
	});

	// Get the images for the contest
	// store them in an array so that we can use .push() after the form is sent
	$scope.participations = [];
	$http.get('api/images/contest/' + contest).success(function(result) {
			angular.forEach(result, function(value, key) {
				$scope.participations.push(value);
				if(value.prize == 1) $scope.results.first = value.id;
				if(value.prize == 2) $scope.results.second = value.id;
				if(value.prize == 3) $scope.results.third = value.id;

			});
	});



	// Function called when form is sent
	$scope.sendVotes = function () {

		alert("VOTING: "+$scope.results);

		// Call the service function that will connect with the API
		ImageParticipation.voteImage($scope.results.first,1)
		// handle success
		.then(function () {
			alert('CONTROLLER: Success');
		})
		// handle error
		.catch(function () {
			//$scope.error = true;
			alert('CONTROLLER: Error');
		});

		ImageParticipation.voteImage($scope.results.second,2)
		// handle success
		.then(function () {
			alert('CONTROLLER: Success');
		})
		// handle error
		.catch(function () {
			//$scope.error = true;
			alert('CONTROLLER: Error');
		});

		ImageParticipation.voteImage($scope.results.third,3)
		// handle success
		.then(function () {
			alert('CONTROLLER: Success');
		})
		// handle error
		.catch(function () {
			//$scope.error = true;
			alert('CONTROLLER: Error');
		});


			alert("VOTING: Done");
	};

}]);
