/**
 * Created by nitinpasumarthy on 6/7/16.
 */

class Logger {
    constructor() {

    }

    info(e) {
        console.log(e.message, e.data)
    }

    warn(e) {
        console.log(e.message, e.data)
    }

    error(e) {
        console.log(e.message, e.data)
    }
}

let app = angular.module('milestones', []);

