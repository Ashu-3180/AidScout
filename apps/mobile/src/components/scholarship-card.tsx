import { StyleSheet, Text, View } from 'react-native';

import type { Scholarship } from '@/data/scholarships';

export function ScholarshipCard({ scholarship }: { scholarship: Scholarship }) {
  return <View accessibilityRole="summary" style={styles.card}>
    <View style={styles.categoryPill}><Text style={styles.category}>{scholarship.category}</Text></View>
    <Text style={styles.title}>{scholarship.title}</Text><Text style={styles.description}>{scholarship.description}</Text>
    <View style={styles.detailGrid}><View style={styles.detail}><Text style={styles.detailLabel}>Funding</Text><Text style={styles.detailValue}>{scholarship.funding}</Text></View><View style={styles.detail}><Text style={styles.detailLabel}>Deadline</Text><Text style={styles.detailValue}>{scholarship.deadline}</Text></View></View>
    <View style={styles.divider} /><Text style={styles.audience}>{scholarship.audience}</Text><Text style={styles.source}>{scholarship.source}</Text>
  </View>;
}

const styles = StyleSheet.create({
  card: { backgroundColor: '#FFFFFF', borderColor: '#E3E8F2', borderWidth: 1, borderRadius: 20, padding: 20, gap: 10, shadowColor: '#101C35', shadowOpacity: 0.05, shadowRadius: 12, elevation: 2 }, categoryPill: { alignSelf: 'flex-start', backgroundColor: '#DDF7ED', borderRadius: 99, paddingHorizontal: 10, paddingVertical: 5 }, category: { color: '#176B4A', fontSize: 12, fontWeight: '700' }, title: { color: '#101C35', fontSize: 20, fontWeight: '800', lineHeight: 26 }, description: { color: '#53627A', fontSize: 14, lineHeight: 21 }, detailGrid: { flexDirection: 'row', gap: 16, marginTop: 4 }, detail: { flex: 1, gap: 3 }, detailLabel: { color: '#6B7890', fontSize: 12, fontWeight: '700', textTransform: 'uppercase', letterSpacing: 0.4 }, detailValue: { color: '#273652', fontSize: 13, lineHeight: 19, fontWeight: '600' }, divider: { height: 1, backgroundColor: '#E9EDF5', marginTop: 2 }, audience: { color: '#273652', fontSize: 13, fontWeight: '700', lineHeight: 19 }, source: { color: '#6B7890', fontSize: 12, lineHeight: 18 },
});
