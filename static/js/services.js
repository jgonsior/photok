var photokServices = angular.module('photokServices', ['ngResource']);

photokServices.factory('ImageParticipation', ['$q', '$timeout', '$http',
function ($q, $timeout, $http){
	return ({
      sendImage: sendImage
    });

	function sendImage(title, path, exif, contest, user) {
		var deferred = $q.defer();
		$http.post('/api/images/contest/1', {title: title, path: path, exifData: exif, contestId: contest, userId: user, prize: "Nothing"})
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

	function createContest(headline, workingTitle) {
		var deferred = $q.defer();
		$http.post('/api/contests', {headline: headline, workingTitle: workingTitle, startDate: "2016-01-12 13:01:54.411227",endDate:"2016-01-12 13:01:54.411227", createdDate: "2016-01-12 13:01:54.411227", voteMethod: "simple"})
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

	function editContest(id, headline, workingTitle) {
		var deferred = $q.defer();
		$http.put('/api/contests/'+id, {headline: headline, workingTitle: workingTitle, startDate: "2016-01-12 13:01:54.411227",endDate:"2016-01-12 13:01:54.411227", createdDate: "2016-01-12 13:01:54.411227", voteMethod: "simple"})
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
