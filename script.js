// Grammar 데이터 생성 (G01 ~ G80)
const grammarData = {
  stage1: [
    { id: 'G01', title: 'Present Simple' },
    { id: 'G02', title: 'Past Simple' },
    { id: 'G03', title: 'Future Simple' },
    { id: 'G04', title: 'Present Continuous' },
    { id: 'G05', title: 'Past Continuous' },
    { id: 'G06', title: 'Present Perfect' },
    { id: 'G07', title: 'Past Perfect' },
    { id: 'G08', title: 'Countable Nouns' },
    { id: 'G09', title: 'Uncountable Nouns' },
    { id: 'G10', title: 'Articles (a, an, the)' },
    { id: 'G11', title: 'Pronouns' },
    { id: 'G12', title: 'Possessive Adjectives' },
    { id: 'G13', title: 'Possessive Pronouns' },
    { id: 'G14', title: 'Demonstratives' },
    { id: 'G15', title: 'Question Words' },
    { id: 'G16', title: 'Yes/No Questions' },
    { id: 'G17', title: 'Wh- Questions' },
    { id: 'G18', title: 'Negation' },
    { id: 'G19', title: 'Imperative' },
    { id: 'G20', title: 'There is/There are' },
    { id: 'G21', title: 'Have/Has' },
    { id: 'G22', title: 'Do/Does' },
    { id: 'G23', title: 'Can/Could' },
    { id: 'G24', title: 'Must/Should' },
    { id: 'G25', title: 'May/Might' },
    { id: 'G26', title: 'Adjectives' },
    { id: 'G27', title: 'Comparative Adjectives' },
    { id: 'G28', title: 'Superlative Adjectives' },
    { id: 'G29', title: 'Adverbs' },
    { id: 'G30', title: 'Prepositions' }
  ],
  stage2: [
    { id: 'G31', title: 'Present Perfect Continuous' },
    { id: 'G32', title: 'Past Perfect Continuous' },
    { id: 'G33', title: 'Future Continuous' },
    { id: 'G34', title: 'Future Perfect' },
    { id: 'G35', title: 'Conditional Sentences (Type 1)' },
    { id: 'G36', title: 'Conditional Sentences (Type 2)' },
    { id: 'G37', title: 'Conditional Sentences (Type 3)' },
    { id: 'G38', title: 'Relative Clauses (Who/Which/That)' },
    { id: 'G39', title: 'Relative Clauses (Whose/Where/When)' },
    { id: 'G40', title: 'Reported Speech (Statements)' },
    { id: 'G41', title: 'Reported Speech (Questions)' },
    { id: 'G42', title: 'Passive Voice (Present)' },
    { id: 'G43', title: 'Passive Voice (Past)' },
    { id: 'G44', title: 'Passive Voice (Future)' },
    { id: 'G45', title: 'Gerunds' },
    { id: 'G46', title: 'Infinitives' },
    { id: 'G47', title: 'Gerunds vs Infinitives' },
    { id: 'G48', title: 'Participles' },
    { id: 'G49', title: 'Phrasal Verbs (Type 1)' },
    { id: 'G50', title: 'Phrasal Verbs (Type 2)' },
    { id: 'G51', title: 'Conjunction: And/But/Or' },
    { id: 'G52', title: 'Conjunction: Because/Although' },
    { id: 'G53', title: 'Conjunction: If/Unless' },
    { id: 'G54', title: 'Articles (Advanced)' },
    { id: 'G55', title: 'Quantifiers (Some/Any/Much/Many)' },
    { id: 'G56', title: 'Quantifiers (Few/Little/Several)' },
    { id: 'G57', title: 'Pronouns (Reflexive)' },
    { id: 'G58', title: 'Pronouns (Reciprocal)' },
    { id: 'G59', title: 'Word Order' },
    { id: 'G60', title: 'Emphasis & Inversion' }
  ],
  stage3: [
    { id: 'G61', title: 'Cleft Sentences' },
    { id: 'G62', title: 'Hedging Language' },
    { id: 'G63', title: 'Discourse Markers' },
    { id: 'G64', title: 'Nominalization' },
    { id: 'G65', title: 'Complex Sentence Structures' },
    { id: 'G66', title: 'Reduced Relative Clauses' },
    { id: 'G67', title: 'Absolute Phrases' },
    { id: 'G68', title: 'Modal Verbs (Advanced)' },
    { id: 'G69', title: 'Semi-Modal Verbs' },
    { id: 'G70', title: 'Subjunctive Mood' },
    { id: 'G71', title: 'Causative Verbs' },
    { id: 'G72', title: 'Perception Verbs' },
    { id: 'G73', title: 'Verb Patterns & Complements' },
    { id: 'G74', title: 'Fronting & Topicalization' },
    { id: 'G75', title: 'Apposition' },
    { id: 'G76', title: 'Ellipsis & Substitution' },
    { id: 'G77', title: 'Cohesion & Coherence' },
    { id: 'G78', title: 'Register & Style' },
    { id: 'G79', title: 'Idioms & Collocations' },
    { id: 'G80', title: 'Advanced Sentence Combining' }
  ]
};

// 그리드 생성 함수
function generateGrammarGrid(containerId, data) {
  const container = document.getElementById(containerId);
  
  data.forEach(item => {
    const link = document.createElement('a');
    link.href = `#${item.id}`;
    link.className = 'g-link';
    link.innerHTML = `
      <span class="g-num">${item.id}</span>
      <span class="g-title">${item.title}</span>
    `;
    container.appendChild(link);
  });
}

// 페이지 로드 시 그리드 생성
document.addEventListener('DOMContentLoaded', () => {
  generateGrammarGrid('grid1', grammarData.stage1);
  generateGrammarGrid('grid2', grammarData.stage2);
  generateGrammarGrid('grid3', grammarData.stage3);
});
