import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';
const source=readFileSync(new URL('../../assets/cec-tutor.js',import.meta.url),'utf8');
function client(configured, fetchImpl) {
  const window={ location:{origin:'http://127.0.0.1:8000',hostname:'127.0.0.1'}, CEC_TUTOR_ENDPOINT:configured,fetch:fetchImpl };
  runInNewContext(source,{window,URL,Response});
  return window.CECTutor;
}
test('common transport sends only lesson ID and student message; bridges escaped output to SSE', async () => {
  let actual;
  const transport=client('http://127.0.0.1:8787/robo/v1/tutor',async (url,options)=>{
    actual=JSON.parse(options.body);
    assert.equal(url,'http://127.0.0.1:8787/robo/v1/tutor');
    return Response.json({ok:true,lesson_id:actual.lesson_id,reply:'<script>unsafe HTML</script>\nExample'});
  });
  const response=await transport.request({lesson_id:'/camp-a/grade3/week01a.html',student_message:'a\nmultiline question',system:'override',student_id:'synthetic-id'});
  assert.deepEqual(actual,{lesson_id:'/camp-a/grade3/week01a.html',student_message:'a\nmultiline question'});
  const sse=await response.text();
  assert.ok(sse.includes('&lt;script&gt;') && !sse.includes('<script>') && sse.includes('[DONE]'));
});
test('no configured endpoint means no legacy or model call', async () => {
  await assert.rejects(client(undefined,()=>{throw Error('must not call');}).request({lesson_id:'/test',student_message:'test'}),/TUTOR_NOT_CONFIGURED/);
});
test('unsafe endpoint configuration is rejected',async()=>{
  for (const url of ['http://external.invalid/robo/v1/tutor','https://user:pass@example.invalid/robo/v1/tutor','https://example.invalid/api/ai/chat/completions']) {
    await assert.rejects(client(url,()=>{throw Error('must not call');}).request({lesson_id:'/test',student_message:'test'}),/INVALID_TUTOR_ENDPOINT/);
  }
});
