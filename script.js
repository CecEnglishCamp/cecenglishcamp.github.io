// ===== DROPDOWN MENU CONTROL =====
function initDropdown() {
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        const btn = dropdown.querySelector('.btn-box');
        
        if (!btn) return;

        // Click to toggle (mobile)
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            
            // Close other dropdowns
            document.querySelectorAll('.dropdown.active').forEach(d => {
                if (d !== dropdown) d.classList.remove('active');
            });
            
            dropdown.classList.toggle('active');
        });
        
        // Desktop: hover
        dropdown.addEventListener('mouseenter', () => {
            if (window.innerWidth > 768) {
                dropdown.classList.add('active');
            }
        });
        
        dropdown.addEventListener('mouseleave', () => {
            if (window.innerWidth > 768) {
                dropdown.classList.remove('active');
            }
        });
    });

    // Close all dropdowns when clicking elsewhere
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown.active').forEach(d => {
                d.classList.remove('active');
            });
        }
    });
}

// ===== GRAMMAR MAPPING DATA =====
const grammarMapping = {
    1: {p: "G01/G01_be_verb_present_tense.html", t: "Be Verb – Present"},
    2: {p: "G02/G02_articles_a,_an,_the.html", t: "Articles (a, an, the)"},
    3: {p: "G03/G03_simple_present_tense.html", t: "Simple Present"},
    4: {p: "G04/G04_present_continuous_tense.html", t: "Present Continuous"},
    5: {p: "G05/G05_simple_past_tense.html", t: "Simple Past"},
    6: {p: "G06/G06_future_tense_will_going_to.html", t: "Future Tense"},
    7: {p: "G07/G07_modal_verbs_can,_could,_should.html", t: "Modal Verbs"},
    8: {p: "G08/G08_countable_vs_uncountable_nouns.html", t: "Countable/Uncountable"},
    9: {p: "G09/G09_question_formation_wh-questions.html", t: "WH-Questions"},
    10: {p: "G10/G10_comparative_and_superlative.html", t: "Comparatives"},
    11: {p: "G11/G11_possessive_forms_my,_your,_his,_her.html", t: "Possessive Forms"},
    12: {p: "G12/G12_there_is___there_are.html", t: "There is / There are"},
    13: {p: "G13/G13_prepositions_of_place_in,_on,_at.html", t: "Prep of Place"},
    14: {p: "G14/G14_prepositions_of_time.html", t: "Prep of Time"},
    15: {p: "G15/G15_demonstratives_this,_that,_these,_those.html", t: "Demonstratives"},
    16: {p: "G16/G16_plural_nouns_regular_and_irregular.html", t: "Plural Nouns"},
    17: {p: "G17/G17_object_pronouns_me,_you,_him,_her.html", t: "Object Pronouns"},
    18: {p: "G18/G18_yes_no_questions_and_short_answers.html", t: "Yes/No Questions"},
    19: {p: "G19/G19_frequency_adverbs_always,_sometimes,_never.html", t: "Frequency Adverbs"},
    20: {p: "G20/G20_basic_imperative_commands.html", t: "Imperatives"},
    21: {p: "G21/G21_past_continuous_tense.html", t: "Past Continuous"},
    22: {p: "G22/G22_present_perfect_simple_introduction.html", t: "Present Perfect"},
    23: {p: "G23/G23_modal_verbs_must,_have_to,_need_to.html", t: "Must/Have to"},
    24: {p: "G24/G24_some,_any,_no,_none.html", t: "Some, Any, No"},
    25: {p: "G25/G25_adverbs_of_manner_-ly_adverbs.html", t: "Adverbs of Manner"},
    26: {p: "G26/G26_conjunctions_and,_but,_or,_so.html", t: "Conjunctions"},
    27: {p: "G27/G27_like_vs_would_like.html", t: "Like vs Would Like"},
    28: {p: "G28/G28_too_vs_enough.html", t: "Too vs Enough"},
    29: {p: "G29/G29_first_conditional_if_+_will.html", t: "First Conditional"},
    30: {p: "G30/G30_gerunds_vs_infinitives_basic.html", t: "Gerunds/Infinitives"},
    31: {p: "G31/G31_relative_pronouns_who,_which,_that.html", t: "Relative Pronouns"},
    32: {p: "G32/G32_past_simple_vs_past_continuous.html", t: "Past Simple vs Cont"},
    33: {p: "G33/G33_used_to_vs_be_used_to.html", t: "Used to / Be Used to"},
    34: {p: "G34/G34_question_tags.html", t: "Question Tags"},
    35: {p: "G35/G35_reflexive_pronouns_myself,_yourself.html", t: "Reflexive Pronouns"},
    36: {p: "G36/G36_each_vs_every.html", t: "Each vs Every"},
    37: {p: "G37/G37_both,_either,_neither.html", t: "Both, Either, Neither"},
    38: {p: "G38/G38_so_vs_such.html", t: "So vs Such"},
    39: {p: "G39/G39_still,_yet,_already.html", t: "Still, Yet, Already"},
    40: {p: "G40/G40_direct_vs_indirect_speech_basic.html", t: "Direct/Indirect Speech"},
    41: {p: "G41/G41_present_perfect_vs_past_simple.html", t: "Pres Perfect vs Past"},
    42: {p: "G42/G42_present_perfect_continuous.html", t: "Pres Perfect Cont"},
    43: {p: "G43/G43_past_perfect_simple.html", t: "Past Perfect"},
    44: {p: "G44/G44_future_perfect.html", t: "Future Perfect"},
    45: {p: "G45/G45_modal_verbs_might,_may,_could_for_possibility.html", t: "Modals of Possibility"},
    46: {p: "G46/G46_second_conditional_if_+_would.html", t: "Second Conditional"},
    47: {p: "G47/G47_third_conditional_if_+_had_+_would_have.html", t: "Third Conditional"},
    48: {p: "G48/G48_passive_voice_present_and_past.html", t: "Passive Voice"},
    49: {p: "G49/G49_causative_verbs_have,_get,_make,_let.html", t: "Causative Verbs"},
    50: {p: "G50/G50_gerunds_and_infinitives_advanced.html", t: "Gerunds/Infinitives 2"},
    51: {p: "G51/G51_phrasal_verbs_separable_and_inseparable.html", t: "Phrasal Verbs"},
    52: {p: "G52/G52_relative_clauses_defining_and_non-defining.html", t: "Relative Clauses"},
    53: {p: "G53/G53_reported_speech_statements_and_questions.html", t: "Reported Speech"},
    54: {p: "G54/G54_wish_and_if_only.html", t: "Wish and If Only"},
    55: {p: "G55/G55_articles_advanced_usage.html", t: "Articles Adv"},
    56: {p: "G56/G56_quantifiers_much_many_few_little.html", t: "Quantifiers"},
    57: {p: "G57/G57_linking_words_however,_therefore,_although.html", t: "Linking Words"},
    58: {p: "G58/G58_emphasis_do_does_did_for_emphasis.html", t: "Emphatic Do"},
    59: {p: "G59/G59_cleft_sentences_it_is..._who_that.html", t: "Cleft Sentences"},
    60: {p: "G60/G60_mixed_conditionals.html", t: "Mixed Conditionals"},
    61: {p: "G61/G61_future_in_the_past_was_going_to.html", t: "Future in the Past"},
    62: {p: "G62/G62_participle_clauses.html", t: "Participle Clauses"},
    63: {p: "G63/G63_inversion_advanced_word_order.html", t: "Inversion"},
    64: {p: "G64/G64_subjunctive_mood.html", t: "Subjunctive Mood"},
    65: {p: "G65/G65_double_comparatives_the_more..._the_more.html", t: "Double Comparatives"},
    66: {p: "G66/G66_advanced_passive_voice_all_tenses.html", t: "Passive Voice Part 1"},
    67: {p: "G67/G67_modals_of_deduction_must_have,_can't_have.html", t: "Modals of Deduction"},
    68: {p: "G68/G68_advanced_conditionals_unless,_provided_that.html", t: "Adv Conditionals"},
    69: {p: "G69/G69_nominal_clauses_that-clauses.html", t: "Nominal Clauses"},
    70: {p: "G70/G70_advanced_relative_clauses.html", t: "Adv Relative Clauses"},
    71: {p: "G71/G71_complex_phrasal_verbs.html", t: "Complex Phrasal Verbs"},
    72: {p: "G72/G72_advanced_reported_speech.html", t: "Adv Reported Speech"},
    73: {p: "G73/G73_ellipsis_and_substitution.html", t: "Ellipsis"},
    74: {p: "G74/G74_advanced_linking_devices.html", t: "Linking Devices"},
    75: {p: "G75/G75_hedging_language_seems,_appears,_tend_to.html", t: "Hedging Language"},
    76: {p: "G76/G76_fronting_and_inversion.html", t: "Fronting"},
    77: {p: "G77/G77_complex_sentence_structures.html", t: "Complex Sentences"},
    78: {p: "G78/G78_advanced_gerunds_and_infinitives.html", t: "Adv Gerunds"},
    79: {p: "G79/G79_nominalization.html", t: "Nominalization"},
    80: {p: "G80/G80_advanced_articles_and_determiners.html", t: "Adv Articles"}
};

const baseURL = "https://cecenglishcamp.github.io/B_Camp/GrammarBaseCamp/";

// ===== RENDER GRAMMAR GRID =====
function renderGrammarGrid(start, end, gridId) {
    const grid = document.getElementById(gridId);
    if (!grid) return;

    for (let i = start; i <= end; i++) {
        const gNum = i < 10 ? 'G0' + i : 'G' + i;
        const item = grammarMapping[i];
        if (!item) continue;

        const link = document.createElement('a');
        link.href = baseURL + item.p;
        link.target = '_blank';
        link.className = 'g-link';
        link.innerHTML = `<span class="g-num">${gNum}</span><span class="g-title">${item.t}</span>`;
        grid.appendChild(link);
    }
}

// ===== INITIALIZE =====
document.addEventListener('DOMContentLoaded', () => {
    initDropdown();
    renderGrammarGrid(1, 30, 'grid1');
    renderGrammarGrid(31, 60, 'grid2');
    renderGrammarGrid(61, 80, 'grid3');
});
