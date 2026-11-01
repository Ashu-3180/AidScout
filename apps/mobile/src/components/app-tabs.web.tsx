import type { ComponentProps } from 'react';

import {
  Tabs,
  TabList,
  TabTrigger,
  TabSlot,
  TabTriggerSlotProps,
  TabListProps,
} from 'expo-router/ui';
import { Pressable, Text, View, StyleSheet } from 'react-native';

import { MaxContentWidth, Spacing } from '@/constants/theme';


export default function AppTabs() {
  return (
    <Tabs>
      <TabSlot style={{ height: '100%' }} />
      <TabList asChild>
        <CustomTabList>
          <TabTrigger name="home" href="/" asChild>
            <TabButton>Home</TabButton>
          </TabTrigger>
          <TabTrigger name="explore" href="/explore" asChild>
            <TabButton>Explore</TabButton>
          </TabTrigger>
        </CustomTabList>
      </TabList>
    </Tabs>
  );
}

export function TabButton({ children, isFocused, ...props }: TabTriggerSlotProps) {
  const pressableProps = props as ComponentProps<typeof Pressable>;
  return (
    <Pressable {...pressableProps} style={({ pressed }) => pressed && styles.pressed}>
      <View style={[styles.tabButtonView, isFocused && styles.tabButtonFocused]}>
        <Text style={[styles.tabLabel, isFocused && styles.tabLabelFocused]}>{children}</Text>
      </View>
    </Pressable>
  );
}

export function CustomTabList(props: TabListProps) {
  return (
    <View {...props} style={styles.tabListContainer}>
      <View style={styles.innerContainer}>
        <Text style={styles.brandText}>AidScout</Text>

        {props.children}

        <Text style={styles.previewText}>Frontend preview</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  tabListContainer: {
    position: 'absolute',
    width: '100%',
    padding: Spacing.three,
    justifyContent: 'center',
    alignItems: 'center',
    flexDirection: 'row',
  },
  innerContainer: {
    paddingVertical: 10,
    paddingHorizontal: Spacing.four,
    borderRadius: 16,
    flexDirection: 'row',
    alignItems: 'center',
    flexGrow: 1,
    gap: 4,
    maxWidth: MaxContentWidth,
    backgroundColor: '#101C35',
  },
  brandText: {
    marginRight: 'auto', color: '#FFFFFF', fontSize: 20, fontWeight: '900',
  },
  pressed: {
    opacity: 0.7,
  },
  tabButtonView: {
    paddingVertical: 8,
    paddingHorizontal: Spacing.three,
    borderRadius: 10,
  },
  tabButtonFocused: {
    backgroundColor: '#315BE8',
  },
  tabLabel: {
    color: '#D2DAE9', fontSize: 14, fontWeight: '700',
  },
  tabLabelFocused: {
    color: '#FFFFFF',
  },
  previewText: {
    color: '#AAB8D0', fontSize: 12, fontWeight: '600', marginLeft: Spacing.two,
  },
});
