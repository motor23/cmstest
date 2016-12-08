import {expect} from 'chai';
import {flatten, compile, match} from '../../src/js/util/router';


describe('flatten', function () {
    it('return flattened path list', function () {
        expect(flatten([])).to.deep.equal([]);

        expect(flatten([
            {path: '/', children: 1, onEnter: [], onLeave: []}
        ])).to.deep.equal([
            {path: '/', children: 1, onEnter: [], onLeave: []}
        ]);

        expect(flatten([
            {path: '/', children: 1},
            {path: '/:stream', onEnter: [1], children: [
                {path: '/', children: 2},
                {path: '/:id', onEnter: [2], children: [
                    {path: '/', children: 3},
                    {path: '/log', onEnter: [3], children: [
                        {path: '/', onEnter: [4], children: 4},
                        {path: '/:date', children: 5}
                    ]}
                ]}
            ]}
        ])).to.deep.equal([
            {path: '/', children: 1, onEnter: [], onLeave: []},
            {path: '/:stream/', children: 2, onEnter: [1], onLeave: []},
            {path: '/:stream/:id/', children: 3, onEnter: [1, 2], onLeave: []},
            {path: '/:stream/:id/log/', children: 4, onEnter: [1, 2, 3, 4], onLeave: []},
            {path: '/:stream/:id/log/:date', children: 5, onEnter: [1, 2, 3], onLeave: []}
        ])
    });
});


describe('compile', function () {
    it('parse path pattern', function () {
        expect(compile('/')).to.eql({pattern: '/', re: '^/$', names: [], tokens: ['/']});
        expect(compile('/:stream')).to.eql({pattern: '/:stream', re: '^/([^/]+)$', names: ['stream'], tokens: ['/', ':stream']});
        expect(compile('/*')).to.eql({pattern: '/*', re: '^/(.*)$', names: ['splat'], tokens: ['/', '*']})
    });
});


describe('match', function () {
    it('match pathname against pattern', function () {
        expect(match('foo', 'bar')).eql(null);
        expect(match('/', '/')).eql({names: [], values: []});
        expect(match('/:stream', '/docs')).eql({names: ['stream'], values: ['docs']});
        expect(match('/:stream/:id', '/docs/42')).eql({names: ['stream', 'id'], values: ['docs', '42']});
        expect(match('/:stream/:id/log', '/docs/42')).eql(null);
        expect(match('/:stream/:id/log', '/docs/42/log')).eql({names: ['stream', 'id'], values: ['docs', '42']});
        expect(match('*', 'foo/bar')).eql({names: ['splat'], values: ['foo/bar']});
        expect(match('/:stream/*', '/docs/42/log')).eql({names: ['stream', 'splat'], values: ['docs', '42/log']});
    });
});