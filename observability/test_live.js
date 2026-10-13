// Offline behavior checks for partial evidence, safe narration and measured final results.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname,'static/app.js'),'utf8');
const {eventStory, liveWorkflow} = vm.runInNewContext(source.split('function render(){')[0]+'\n({eventStory,liveWorkflow})');
const partial = {trace:[{kind:'inference',name:'original / question 1'}],harness:[],calls:[{
 context:'original',question_index:1,input:'Test question',ground_truth:'reference',
 response:{text:'<script>alert("unsafe")</script>',usage:{prompt_tokens:12,completion_tokens:3},seconds:2}}]};
assert.equal(eventStory(partial.trace[0],partial)[1],partial.calls[0].response.text);
const html = liveWorkflow(partial);
assert.ok(html.includes('&lt;script&gt;'));
assert.ok(!html.includes('<script>'));
assert.ok(!html.includes('Final measured results'));
assert.ok(html.includes('1 completed comparison calls'));
assert.ok(liveWorkflow({trace:[{kind:'workflow_error',message:'Provider unavailable'}]}).includes('Experiment stopped'));
const result=JSON.parse(fs.readFileSync(path.join(__dirname,'../evaluation/results/llmlingua-20261013-03/result.json')));
const final=liveWorkflow({result,trace:[{kind:'workflow_end'}],calls:[]});
assert.ok(final.includes('42.10%'));
assert.ok(final.includes('7,817'));
assert.ok(final.includes('Reasoning tokens'));
assert.ok(final.includes('7,499'));
assert.ok(final.includes('included in output'));
assert.ok(final.includes('used more output tokens'));
assert.ok(final.includes('Final measured results'));
assert.ok(final.includes('Compare the answers with human references'));
console.log('Live workflow checks passed: partial outputs, escaping, failure state and final tradeoffs.');
