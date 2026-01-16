// ===== DROPDOWN 기능 =====
document.querySelectorAll('.dropdown').forEach(dropdown => {
  const btn = dropdown.querySelector('.btn-box');
  
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    
    // 다른 드롭다운 닫기
    document.querySelectorAll('.dropdown.active').forEach(d => {
      if (d !== dropdown) d.classList.remove('active');
    });
    
    // 현재 드롭다운 토글
    dropdown.classList.toggle('active');
  });
});

// 문서 클릭 시 드롭다운 닫기
document.addEventListener('click', () => {
  document.querySelectorAll('.dropdown.active').forEach(d => {
    d.classList.remove('active');
  });
});

// ===== GRAMMAR 그리드 생성 =====
const grammarData = {
  stage1: [
    { id: 'G01', title: 'Be Verb – Present Tense', path: './G01/G01_be_verb_present_tense.html' },
    { id: 'G02', title: 'Articles – a, an, the', path: './G02/G02_articles_a,_an,_the.html' },
    { id: 'G03', title: 'Simple Present Tense', path: './G03/G03_simple_present_tense.html' },
    { id: 'G04', title: 'Present Continuous Tense', path: './G04/G04_present_continuous_tense.html' },
    { id: 'G05', title: 'Simple Past Tense', path: './G05/G05_simple_past_tense.html' },
    { id: 'G06', title: 'Future Tense (Will/Going to)', path: './G06/G06_future_tense_will_going_to.html' },
    { id: 'G07', title: 'Modal Verbs (Can/Could/Should)', path: './G07/G07_modal_verbs_can,_could,_should.html' },
    { id: 'G08', title: 'Countable vs Uncountable Nouns', path: './G08/G08_countable_vs_uncountable_nouns.html' },
    { id: 'G09', title: 'WH-Questions', path: './G09/G09_question_formation_wh-questions.html' },
    { id: 'G10', title: 'Comparative and Superlative', path: './G10/G10_comparative_and_superlative.html' },
    { id: 'G11', title: 'Possessive Forms', path: './G11/G11_possessive_forms_my,_your,_his,_her.html' },
    { id: 'G12', title: 'There is / There are', path: './G12/G12_there_is___there_are.html' },
    { id: 'G13', title: 'Prepositions of Place', path: './G13/G13_prepositions_of_place_in,_on,_at.html' },
    { id: 'G14', title: 'Prepositions of Time', path: './G14/G14_prepositions_of_time.html' },
    { id: 'G15', title: 'Demonstratives', path: './G15/G15_demonstratives_this,_that,_these,_those.html' },
    { id: 'G16', title: 'Plural Nouns', path: './G16/G16_plural_nouns_regular_and_irregular.html' },
    { id: 'G17', title: 'Object Pronouns', path: './G17/G17_object_pronouns_me,_you,_him,_her.html' },
    { id: 'G18', title: 'Yes/No Questions', path: './G18/G18_yes_no_questions_and_short_answers.html' },
    { id: 'G19', title: 'Frequency Adverbs', path: './G19/G19_frequency_adverbs_always,_sometimes,_never.html' },
    { id: 'G20', title: 'Basic Imperative Commands', path: './G20/G20_basic_imperative_commands.html' },
    { id: 'G21', title: 'Past Continuous Tense', path: './G21/G21_past_continuous_tense.html' },
    { id: 'G22', title: 'Present Perfect Simple', path: './G22/G22_present_perfect_simple_introduction.html' },
    { id: 'G23', title: 'Modal Verbs (Must/Have to)', path: './G23/G23_modal_verbs_must,_have_to,_need_to.html' },
    { id: 'G24', title: 'Some, Any, No, None', path: './G24/G24_some,_any,_no,_none.html' },
    { id: 'G25', title: 'Adverbs of Manner', path: './G25/G25_adverbs_of_manner_-ly_adverbs.html' },
    { id: 'G26', title: 'Conjunctions', path: './G26/G26_conjunctions_and,_but,_or,_so.html' },
    { id: 'G27', title: 'Like vs Would Like', path: './G27/G27_like_vs_would_like.html' },
    { id: 'G28', title: 'Too vs Enough', path: './G28/G28_too_vs_enough.html' },
    { id: 'G29', title: 'First Conditional', path: './G29/G29_first_conditional_if_+_will.html' },
    { id: 'G30', title: 'Gerunds vs Infinitives', path: './G30/G30_gerunds_vs_infinitives_basic.html' }
  ],
  stage2: [
    { id: 'G31', title: 'Relative Pronouns', path: './G31/G31_relative_pronouns_who,_which,_that.html' },
    { id: 'G32', title: 'Past Simple vs Past Continuous', path: './G32/G32_past_simple_vs_past_continuous.html' },
    { id: 'G33', title: 'Used to vs Be Used to', path: './G33/G33_used_to_vs_be_used_to.html' },
    { id: 'G34', title: 'Question Tags', path: './G34/G34_question_tags.html' },
    { id: 'G35', title: 'Reflexive Pronouns', path: './G35/G35_reflexive_pronouns_myself,_yourself.html' },
    { id: 'G36', title: 'Each vs Every', path: './G36/G36_each_vs_every.html' },
    { id: 'G37', title: 'Both, Either, Neither', path: './G37/G37_both,_either,_neither.html' },
    { id: 'G38', title: 'So vs Such', path: './G38/G38_so_vs_such.html' },
    { id: 'G39', title: 'Still, Yet, Already', path: './G39/G39_still,_yet,_already.html' },
    { id: 'G40', title: 'Direct vs Indirect Speech', path: './G40/G40_direct_vs_indirect_speech_basic.html' },
    { id: 'G41', title: 'Present Perfect vs Past Simple', path: './G41/G41_present_perfect_vs_past_simple.html' },
    { id: 'G42', title: 'Present Perfect Continuous', path: './G42/G42_present_perfect_continuous.html' },
    { id: 'G43', title: 'Past Perfect Simple', path: './G43/G43_past_perfect_simple.html' },
    { id: 'G44', title: 'Future Perfect', path: './G44/G44_future_perfect.html' },
    { id: 'G45', title: 'Modals of Possibility', path: './G45/G45_modal_verbs_might,_may,_could_for_possibility.html' },
    { id: 'G46', title: 'Second Conditional', path: './G46/G46_second_conditional_if_+_would.html' },
    { id: 'G47', title: 'Third Conditional', path: './G47/G47_third_conditional_if_+_had_+_would_have.html' },
    { id: 'G48', title: 'Passive Voice', path: './G48/G48_passive_voice_present_and_past.html' },
    { id: 'G49', title: 'Causative Verbs', path: './G49/G49_causative_verbs_have,_get,_make,_let.html' },
    { id: 'G50', title: 'Gerunds & Infinitives (Adv)', path: './G50/G50_gerunds_and_infinitives_advanced.html' },
    { id: 'G51', title: 'Phrasal Verbs', path: './G51/G51_phrasal_verbs_separable_and_inseparable.html' },
    { id: 'G52', title: 'Relative Clauses', path: './G52/G52_relative_clauses_defining_and_non-defining.html' },
    { id: 'G53', title: 'Reported Speech', path: './G53/G53_reported_speech_statements_and_questions.html' },
    { id: 'G54', title: 'Wish & If Only', path: './G54/G54_wish_and_if_only.html' },
    { id: 'G55', title: 'Articles (Advanced)', path: './G55/G55_articles_advanced_usage.html' },
    { id: 'G56', title: 'Quantifiers', path: './G56/G56_quantifiers_much_many_few_little.html' },
    { id: 'G57', title: 'Linking Words', path: './G57/G57_linking_words_however,_therefore,_although.html' },
    { id: 'G58', title: 'Emphasis (Do/Does/Did)', path: './G58/G58_emphasis_do_does_did_for_emphasis.html' },
    { id: 'G59', title: 'Cleft Sentences', path: './G59/G59_cleft_sentences_it_is..._who_that.html' },
    { id: 'G60', title: 'Mixed Conditionals', path: './G60/G60_mixed_conditionals.html' }
  ],
  stage3: [
    { id: 'G61', title: 'Future in the Past', path: './G61/G61_future_in_the_past_was_going_to.html' },
    { id: 'G62', title: 'Participle Clauses', path: './G62/G62_participle_clauses.html' },
    { id: 'G63', title: 'Inversion', path: './G63/G63_inversion_advanced_word_order.html' },
    { id: 'G64', title: 'Subjunctive Mood', path: './G64/G64_subjunctive_mood.html' },
    { id: 'G65', title: 'Double Comparatives', path: './G65/G65_double_comparatives_the_more..._the_more.html' },
    { id: 'G66', title: 'Advanced Passive Voice', path: './G66/G66_advanced_passive_voice_all_tenses.html' },
    { id: 'G67', title: 'Modals of Deduction', path: './G67/G67_modals_of_deduction_must_have,_can't_have.html' },
    { id: 'G68', title: 'Advanced Conditionals', path: './G68/G68_advanced_conditionals_unless,_provided_that.html' },
    { id: 'G69', title: 'Nominal Clauses', path: './G69/G69_nominal_clauses_that-clauses.html' },
    { id: 'G70', title: 'Advanced Relative Clauses', path: './G70/G70_advanced_relative_clauses.html' },
    { id: 'G71', title: 'Complex Phrasal Verbs', path: './G71/G71_complex_phrasal_verbs.html' },
    { id: 'G72', title: 'Advanced Reported Speech', path: './G72/G72_advanced_reported_speech.html' },
    { id: 'G73', title: 'Ellipsis & Substitution', path: './G73/G73_ellipsis_and_substitution.html' },
    { id: 'G74', title: 'Advanced Linking Devices', path: './G74/G74_advanced_linking_devices.html' },
    { id: 'G75', title: 'Hedging Language', path: './G75/G75_hedging_language_seems,_appears,_tend_to.html' },
    { id: 'G76', title: 'Fronting & Inversion', path: './G76/G76_fronting_and_inversion.html' },
    { id: 'G77', title: 'Complex Sentence Structures', path: './G77/G77_complex_sentence_structures.html' },
    { id: 'G78', title: 'Adv. Gerunds & Infinitives', path: './G78/G78_advanced_gerunds_and_infinitives.html' },
    { id: 'G79', title: 'Nominalization', path: './G79/G79_nominalization.html' },
    { id: 'G80', title: 'Adv. Articles & Determiners', path: './G80/G80_advanced_articles_and_determiners.html' }
  ]
};

// 그리드 생성 함수
function generateGrammarGrid(containerId, data) {
  const container = document.getElementById(containerId);
  if (!container) return;
  
  data.forEach(item => {
    const link = document.createElement('a');
    link.href = item.path;
    link.className = 'g-link';
    link.innerHTML = `
      <span class="g-num">${item.id}</span>
      <span class="g-title">${item.title}</span>
    `;
    container.appendChild(link);
  });
}

// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', () => {
  generateGrammarGrid('grid1', grammarData.stage1);
  generateGrammarGrid('grid2', grammarData.stage2);
  generateGrammarGrid('grid3', grammarData.stage3);
});
