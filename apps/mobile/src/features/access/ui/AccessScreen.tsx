import type { PropsWithChildren } from 'react';
import { KeyboardAvoidingView, Platform, ScrollView, StyleSheet, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';

import { accessTheme } from '../theme/accessTheme';
import { AccessBrandLockup } from './AccessBrandLockup';

type AccessScreenProps = PropsWithChildren<{ compact?: boolean }>;

export function AccessScreen({ children, compact = false }: AccessScreenProps) {
  return (
    <SafeAreaView style={styles.safeArea} edges={['top', 'right', 'bottom', 'left']}>
      <StatusBar style="dark" backgroundColor={accessTheme.colors.background} />
      <KeyboardAvoidingView
        style={styles.keyboardAvoiding}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        <View style={styles.topBar}>
          <AccessBrandLockup />
        </View>
        <ScrollView
          style={styles.scroll}
          contentContainerStyle={[
            styles.scrollContent,
            compact ? styles.scrollContentCompact : null,
          ]}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        >
          {children}
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: accessTheme.colors.background,
  },
  keyboardAvoiding: {
    flex: 1,
  },
  topBar: {
    minHeight: 68,
    justifyContent: 'center',
    paddingHorizontal: accessTheme.spacing.lg,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: accessTheme.colors.divider,
  },
  scroll: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: 'center',
    paddingHorizontal: accessTheme.spacing.lg,
    paddingTop: accessTheme.spacing.xl,
    paddingBottom: accessTheme.spacing.xxl,
  },
  scrollContentCompact: {
    justifyContent: 'flex-start',
  },
});
