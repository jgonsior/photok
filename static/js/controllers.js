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
	$http.get('api/contests').success(function(data) {
  	$scope.contests = data;
	});

	$scope.orderProp = 'createdDate';
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

	$scope.add = function(){
		console.log($scope.participations);
		$scope.participations.push({
			id: 123123,
			title: "title",
			uploadedOn: "?",
			userId: 1
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
				alert('CONTROLLER: Success');
      })
      // handle error
      .catch(function () {
        //$scope.error = true;
        alert('CONTROLLER: Error');
      });

			alert("SENDING: Done");

			$scope.add();
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
