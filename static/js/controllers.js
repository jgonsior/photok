var photokControllers = angular.module('photokControllers', [
	'contestServices'
]);


photokControllers.controller('HeaderController', ['$scope', '$location',
function($scope, $location) {
	$scope.isActive = function (viewLocation) {
			return viewLocation === $location.path();
	};
}]);

photokControllers.controller('ContestListController', ['$scope', 'Contest',
function($scope, Contest) {
	$scope.contests = Contest.query();
	$scope.orderProp = 'createdDate';
}]);

photokControllers.controller('ContestDetailController', ['$scope', '$routeParams', 'Contest', 'ContestImages','ImageParticipation',
function($scope, $routeParams, Contest, ContestImages, ImageParticipation) {
	$scope.contest = Contest.get({contestId: $routeParams.contestId}, function(contest) {
	});
	$scope.images = ContestImages.get({contestId: $routeParams.contestId}, function(contest) {
	});

	// - - - Form for participation
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
	// - - -

	$scope.sendImage = function () {

		alert("SENDING: "+$scope.participation.title);
		alert("got image: "+$scope.participation.image);

    // generate a token functions TODO: move this somewhere else?
    var rand = function() {
        return Math.random().toString(36).substr(2); // remove `0.`
    };

    var token = function() {
        return rand();
    };
    // call login from service
    ImageParticipation.sendImage($scope.participation.title, "static/images/"+token(), "exif-fake-data","1","1")
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
}]);
