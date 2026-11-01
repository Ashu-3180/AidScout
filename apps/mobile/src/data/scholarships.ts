/**
 * Local UI fixtures only. These entries are illustrative and unverified;
 * they are not official scholarship listings, eligibility determinations,
 * deadlines, funding amounts, or source links.
 */
export type Scholarship = { id: string; title: string; category: string; audience: string; description: string; funding: string; deadline: string; source: string };

export const scholarshipCategories = [
  { label: 'Undergraduate', icon: '🎓' }, { label: 'STEM', icon: '⚗️' },
  { label: 'Women learners', icon: '✦' }, { label: 'Postgraduate', icon: '📚' },
] as const;

export const illustrativeScholarships: Scholarship[] = [
  { id: 'future-pathways', title: 'Future Pathways Award', category: 'Undergraduate', audience: 'Students exploring undergraduate study options', description: 'An illustrative listing used to demonstrate how opportunities may be compared.', funding: 'Not provided in this illustrative record', deadline: 'To be confirmed', source: 'Illustrative placeholder — not an official source' },
  { id: 'build-in-stem', title: 'Build in STEM Grant', category: 'STEM', audience: 'Learners interested in science, technology, engineering, or maths', description: 'A sample opportunity card. Check an official provider before relying on any detail.', funding: 'Not provided in this illustrative record', deadline: 'To be confirmed', source: 'Illustrative placeholder — not an official source' },
  { id: 'next-chapter', title: 'Next Chapter Learner Fund', category: 'Postgraduate', audience: 'Students considering further study', description: 'A demonstration record showing the information AidScout will organize in future.', funding: 'Not provided in this illustrative record', deadline: 'To be confirmed', source: 'Illustrative placeholder — not an official source' },
  { id: 'women-forward', title: 'Women Forward Study Support', category: 'Women learners', audience: 'Women learners exploring education support', description: 'A sample listing only; it does not represent a confirmed funding programme.', funding: 'Not provided in this illustrative record', deadline: 'To be confirmed', source: 'Illustrative placeholder — not an official source' },
];
