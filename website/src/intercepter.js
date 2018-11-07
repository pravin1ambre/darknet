import fetchIntercept from 'fetch-intercept';


const unregister = fetchIntercept.register({
    request: function (url, config) {
        // Modify the url or config here
        console.log("intercepter called");
        config.headers.token="testing";
        return [url, config];
    },

    requestError: function (error) {
        // Called when an error occurred during another 'request' interceptor call
        return Promise.reject(error);
    },

    response: function (response) {
        // Modify the response object
        return response;
    },

    responseError: function (error) {
        // Handle an fetch error
        return Promise.reject(error);
    }
});

export default unregister;

// Call fetch to see your interceptors in action.
// fetch('http://google.com');

// // Unregister your interceptor
// unregister();