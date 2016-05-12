var contestServices = angular.module('contestServices', ['ngResource']);


contestServices.factory('ImageParticipation', ['$q', '$timeout', '$http',
function ($q, $timeout, $http){
	return ({
      sendImage: sendImage
    });


	function sendImage(title, path, exif, contest, user) {
		var deferred = $q.defer();
		$http.post('/api/images/contest/1', {title: title, path: path, exifData: exif, contestId: contest, userId: user, prize: "Nothing"})
			// handle success
			.success(function (data, status) {
				if(status === 200 /*&& data.result*/){
					image = true;
					//alert('SERVICE: Success');
					deferred.resolve();
				} else {
					//alert('SERVICE: Success, but wrong status returned');
					image = false;
					deferred.reject();
				}
			})
			// handle error
			.error(function (data) {
				//alert('SERVICE: Error');
				image = false;
				deferred.reject();
			});

		// return promise object
		return deferred.promise;
	}
	return null;
}]);

contestServices.factory('Contest', ['$resource',
function($resource){
	return $resource('api/contests/:contestId', {}, {
		query: {method:'GET', params:{contestId:''}, isArray:true}
	});
}]);

contestServices.factory('ContestImages', ['$resource',
function($resource){
	return $resource('api/images/contest/:contestId', {}, {
		query: {method:'GET', params:{contestId:''}, isArray:true}
	});
}]);
