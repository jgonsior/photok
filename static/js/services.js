var photokServices = angular.module('photokServices', ['ngResource', 'ngStorage']);

photokServices.factory('ImageParticipation', ['$q', '$timeout', '$http',
function ($q, $timeout, $http){
	return ({
		sendImage: sendImage,
		voteImage: voteImage
    });

	function sendImage(title, path, exif, contest, user) {
		var deferred = $q.defer();
		$http.post('/api/images/contest/1', {title: title, path: path, exifData: exif, contestId: contest, userId: user, prize: 0})
			// handle success
			.success(function (data, status) {
				if(status === 200){
					image = true;
					deferred.resolve();
				} else {
					image = false;
					deferred.reject();
				}
			})
			// handle error
			.error(function (data) {
				image = false;
				deferred.reject();
			});

		// return promise object
		return deferred.promise;
	}

	function voteImage(id, vote) {
		var deferred = $q.defer();
		$http.put('/api/images/'+id, {prize: vote})
			// handle success
			.success(function (data, status) {
				if(status === 200){
					image = true;
					deferred.resolve();
				} else {
					image = false;
					deferred.reject();
				}
			})
			// handle error
			.error(function (data) {
				image = false;
				deferred.reject();
			});

		// return promise object
		return deferred.promise;
	}

	return null;
}]);

photokServices.factory('Contest', ['$q', '$timeout', '$http','$resource',
function ($q, $timeout, $http, $resource){
	return ({
		createContest: createContest,
		deleteContest: deleteContest,
		editContest: editContest
  });

	function createContest(headline, theme, workingTitle, description, startDate, endDate) {
		var deferred = $q.defer();

		$http.post('/api/contestsPrivate', {headline: headline, theme:theme, workingTitle: workingTitle, description:description, startDate: startDate, endDate: endDate, createdDate: "2016-01-12 13:01:54.411227", voteMethod: "simple"})
			// handle success
			.success(function (data, status) {
				if(status === 200){
					deferred.resolve();
				} else {
					deferred.reject();
				}
			})
			// handle error
			.error(function (data) {
				deferred.reject();
			});

		// return promise object
		return deferred.promise;
	}

	function editContest(id, headline, theme, workingTitle, description, startDate, endDate) {
		var deferred = $q.defer();

		$http.put('/api/contests/'+id, {headline: headline, theme: theme, workingTitle: workingTitle, description: description, startDate: startDate, endDate:endDate, createdDate: "2016-01-12 13:01:54.411227", voteMethod: "simple"})
			// handle success
			.success(function (data, status) {
				if(status === 200){
					deferred.resolve();
				} else {
					deferred.reject();
				}
			})
			// handle error
			.error(function (data) {
				deferred.reject();
			});

		// return promise object
		return deferred.promise;
	}

	function deleteContest(id) {
		var deferred = $q.defer();

		$http.delete('/api/contests/'+id)
			// handle success
			.success(function (data, status) {
					deferred.resolve();
			})
			// handle error
			.error(function (data) {
				deferred.reject();
			});

		// return promise object
		return deferred.promise;
	}



	return null;

}]);

photokServices.factory('ContestImages', ['$resource',
function($resource){
	return $resource('api/images/contest/:contestId', {}, {
		query: {method:'GET', params:{contestId:''}, isArray:true}
	});
}]);


photokServices.factory('AuthenticationService', ['$http', '$localStorage', function($http, $localStorage) {
	return ({
		login: login,
		logout: logout
	});

	function login(username, password, callback) {
		$http.post('auth', {username: username, password:password})
			.success(function(response) {
				if(response.access_token) {
					$localStorage.currentUser = {username: username, access_token: response.access_token};
					callback(true);
				}
			})
			.error(function(response) {
				callback(false);
			});
	}

	function logout() {
		delete $localStorage.currentUser;
	}
}]);
