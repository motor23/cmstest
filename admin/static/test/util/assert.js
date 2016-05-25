import {expect} from 'chai';
import assert from '../../src/js/util/assert';


describe('assert', function () {
    it('not throw exception if condition evaluates to true', function () {
        expect(() => {assert(true, 'message')}).to.not.throw(Error);
    });

    it('throw exception if condition evaluates to false', function () {
        expect(() => {assert(false, 'message')}).to.throw(Error);
    });

    it('can accept %s formating arguments for error message', function () {
        expect(() => {assert(false, '%s %s', 'first', 'second')}).to.throw(/first second/);
    })
});