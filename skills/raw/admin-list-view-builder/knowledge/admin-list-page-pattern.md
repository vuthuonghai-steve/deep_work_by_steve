# admin-list-page-pattern — Flutter Clean Architecture List Page Pattern

> **Usage**: Read at Boot Sequence (Tier 1). This file is the single source of truth for list-page-specific patterns. Required before writing any generated code.

---

## 1. BLoC Structure (bloc/)

### 1.1 `<entity>_bloc.dart`

```dart
// TEMPLATE: bloc/<entity>_bloc.dart
// @param {String} entityName — PascalCase, e.g. "Order"
// @param {String} entitySnake — snake_case, e.g. "order"
// @param {PaginationType} paginationType — offset (default)

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:equatable/equatable.dart';
import '../../domain/repositories/<entity>_repository.dart';
import 'package:ktx_app/core/network/paging/paging_model.dart';

class <Entity>ListBloc extends Bloc<<Entity>ListEvent, <Entity>ListState> {
  final <Entity>Repository repository;

  <Entity>ListBloc({required this.repository}) : super(<Entity>ListInitial()) {
    on<Load<Entity>List>(_onLoad);
    on<Filter<Entity>ByStatus>(_onFilterByStatus);
    on<Refresh<Entity>List>(_onRefresh);
  }

  Future<void> _onLoad(Load<Entity>List event, Emitter<<Entity>ListState> emit) async {
    emit(<Entity>ListLoading());
    try {
      final result = await repository.getList(
        page: event.page ?? 1,
        status: event.status,
      );
      emit(<Entity>ListLoaded(
        items: result.items,
        currentPage: result.currentPage,
        totalPages: result.totalPages,
        status: event.status,
      ));
    } catch (e) {
      emit(<Entity>ListError(message: e.toString()));
    }
  }

  Future<void> _onFilterByStatus(Filter<Entity>ByStatus event, Emitter<<Entity>ListState> emit) async {
    add(Load<Entity>List(status: event.status));
  }

  Future<void> _onRefresh(Refresh<Entity>List event, Emitter<<Entity>ListState> emit) async {
    final currentState = state;
    if (currentState is <Entity>ListLoaded) {
      add(Load<Entity>List(status: currentState.currentStatus, page: 1));
    }
  }
}
```

### 1.2 `<entity>_event.dart`

```dart
// TEMPLATE: bloc/<entity>_event.dart

part of '<entity>_bloc.dart';

sealed class <Entity>ListEvent extends Equatable {
  const <Entity>ListEvent();
  @override
  List<Object?> get props => [];
}

final class Load<Entity>List extends <Entity>ListEvent {
  final int? page;
  final String? status;

  const Load<Entity>List({this.page, this.status});

  @override
  List<Object?> get props => [page, status];
}

final class Filter<Entity>ByStatus extends <Entity>ListEvent {
  final String status;

  const Filter<Entity>ByStatus(this.status);

  @override
  List<Object?> get props => [status];
}

final class Refresh<Entity>List extends <Entity>ListEvent {
  const Refresh<Entity>List();
}
```

### 1.3 `<entity>_state.dart`

```dart
// TEMPLATE: bloc/<entity>_state.dart

part of '<entity>_bloc.dart';

sealed class <Entity>ListState extends Equatable {
  const <Entity>ListState();
  @override
  List<Object?> get props => [];
}

final class <Entity>ListInitial extends <Entity>ListState {}

final class <Entity>ListLoading extends <Entity>ListState {}

final class <Entity>ListLoaded extends <Entity>ListState {
  final List<<Entity>Model> items;
  final int currentPage;
  final int totalPages;
  final String? currentStatus;

  const <Entity>ListLoaded({
    required this.items,
    required this.currentPage,
    required this.totalPages,
    this.currentStatus,
  });

  @override
  List<Object?> get props => [items, currentPage, totalPages, currentStatus];
}

final class <Entity>ListError extends <Entity>ListState {
  final String message;

  const <Entity>ListError({required this.message});

  @override
  List<Object?> get props => [message];
}
```

---

## 2. Page Wiring (pages/)

### 2.1 `<entity>_page.dart` — Wiring ONLY

> **Rule**: `*_page.dart` contains ZERO UI widgets. It ONLY provides `BlocProvider` and `Scaffold`.

```dart
// TEMPLATE: pages/<entity>_page.dart
// @param {String} entityName — PascalCase

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:get_it/get_it.dart';
import '../../domain/repositories/<entity>_repository.dart';
import '../bloc/<entity>_bloc.dart';
import '../widgets/<entity>_list_view.dart';

class <Entity>ListPage extends StatelessWidget {
  const <Entity>ListPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => <Entity>ListBloc(
        repository: GetIt.instance<<Entity>Repository>(),
      )..add(const Load<Entity>List()),
      child: Scaffold(
        appBar: AppBar(title: Text('<Entity> List')),
        body: const <Entity>ListView(),
      ),
    );
  }
}
```

---

## 3. Widgets

### 3.1 `<entity>_list_view.dart`

```dart
// TEMPLATE: widgets/<entity>_list_view.dart
// @param {String} entityName
// @param {List<FieldSpec>} cardFields — from Gate 2 confirmation
// @param {List<String>} filterOptions — from Gate 2 confirmation

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../bloc/<entity>_bloc.dart';
import '<entity>_card.dart';
import '<entity>_card_shimmer.dart';
import '<entity>_status_filter_chip.dart';

class <Entity>ListView extends StatelessWidget {
  const <Entity>ListView({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const <<Entity>StatusFilterChip>(),
        Expanded(
          child: BlocBuilder<<Entity>ListBloc, <Entity>ListState>(
            builder: (context, state) {
              return switch (state) {
                <Entity>ListInitial() => const SizedBox.shrink(),
                <Entity>ListLoading() => const <Entity>CardShimmer(),
                <Entity>ListLoaded(:final items) when items.isEmpty =>
                  _EmptyState(),
                <Entity>ListLoaded(:final items) =>
                  _LoadedList(items: items),
                <Entity>ListError(:final message) =>
                  _ErrorState(message: message),
              };
            },
          ),
        ),
      ],
    );
  }
}

class _LoadedList extends StatelessWidget {
  final List<<Entity>Model> items;
  const _LoadedList({required this.items});

  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      padding: const EdgeInsets.all(16),
      itemCount: items.length,
      separatorBuilder: (_, __) => const SizedBox(height: 12),
      itemBuilder: (context, index) => <Entity>Card(item: items[index]),
    );
  }
}

class _EmptyState extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return const Center(child: Text('No data'));
  }
}

class _ErrorState extends StatelessWidget {
  final String message;
  const _ErrorState({required this.message});

  @override
  Widget build(BuildContext context) {
    return Center(child: Text('Error: $message'));
  }
}
```

### 3.2 `<entity>_card.dart`

> **Rule**: Use shared components ONLY. No raw `Color(...)`, `Colors.xxx`, `TextStyle(...)`.

```dart
// TEMPLATE: widgets/<entity>_card.dart
// @param {String} entityName
// @param {List<FieldSpec>} cardFields — confirmed at Gate 2

import 'package:flutter/material.dart';
import '../../data/models/<entity>_model.dart';
import 'package:ktx_app/shared/theme/color_skin.dart';
import 'package:ktx_app/shared/theme/typo_skin.dart';
// ✅ CORRECT: use shared components

class <Entity>Card extends StatelessWidget {
  final <Entity>Model item;
  const <Entity>Card({super.key, required this.item});

  @override
  Widget build(BuildContext context) {
    // @FillIn: use cardFields to render specific fields
    // EXAMPLE structure:
    return Card(
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12.radius),
        side: BorderSide(color: ColorSkin.border()),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // @FillIn: render card fields from Gate 2 confirmed spec
          ],
        ),
      ),
    );
  }
}
```

### 3.3 `<entity>_card_shimmer.dart`

```dart
// TEMPLATE: widgets/<entity>_card_shimmer.dart

import 'package:flutter/material.dart';
import 'package:ktx_app/shared/components/shimmer_widget.dart';
// ✅ CORRECT: use shared shimmer component

class <Entity>CardShimmer extends StatelessWidget {
  const <Entity>CardShimmer({super.key});

  @override
  Widget build(BuildContext context) {
    return ShimmerWidget(
      child: Card(
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12.radius),
        ),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: const [
              ShimmerBox(height: 16, width: 120),
              SizedBox(height: 8),
              ShimmerBox(height: 12, width: 80),
              SizedBox(height: 12),
              ShimmerBox(height: 12),
            ],
          ),
        ),
      ),
    );
  }
}
```

### 3.4 `<entity>_status_filter_chip.dart`

```dart
// TEMPLATE: widgets/<entity>_status_filter_chip.dart
// @param {String} entityName
// @param {List<String>} filterOptions — confirmed at Gate 2

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../bloc/<entity>_bloc.dart';
import 'package:ktx_app/shared/theme/color_skin.dart';

class <Entity>StatusFilterChip extends StatelessWidget {
  const <Entity>StatusFilterChip({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<<Entity>ListBloc, <Entity>ListState>(
      buildWhen: (prev, curr) {
        final prevStatus = prev is <Entity>ListLoaded ? prev.currentStatus : null;
        final currStatus = curr is <Entity>ListLoaded ? curr.currentStatus : null;
        return prevStatus != currStatus;
      },
      builder: (context, state) {
        final selected = state is <Entity>ListLoaded ? state.currentStatus : null;
        final options = ['All', /* @FillIn: from Gate 2 confirmed filterOptions */];

        return SizedBox(
          height: 44,
          child: ListView.separated(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 16),
            itemCount: options.length,
            separatorBuilder: (_, __) => const SizedBox(width: 8),
            itemBuilder: (ctx, i) {
              final opt = options[i];
              final isSelected = (opt == 'All' && selected == null) || opt == selected;
              return FilterChip(
                label: Text(opt),
                selected: isSelected,
                onSelected: (_) {
                  context.read<<Entity>ListBloc>().add(
                    Filter<Entity>ByStatus(opt == 'All' ? '' : opt),
                  );
                },
                selectedColor: ColorSkin.accentBlue(alpha: 0.15),
                checkmarkColor: ColorSkin.accentBlue(),
              );
            },
          ),
        );
      },
    );
  }
}
```

---

## 4. Data Flow & UI States

```
User lands on page
       │
       ▼
┌──────────────────┐
│  <Entity>ListInitial │ → show SizedBox (empty shell)
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  <Entity>ListLoading │ → show <Entity>CardShimmer
└──────────────────┘
       │
  ┌────┴────┐
  │         │
  ▼         ▼
┌──────┐  ┌──────────────┐
│items │  │ <Entity>ListError │
│empty │  └──────────────┘
└──────┘         │
  │               ▼
  ▼         show error + retry
EmptyState widget
```

---

## 5. Constants

### `<entity>_constants.dart`

```dart
// TEMPLATE: constants/<entity>_constants.dart
// @param {String} entityName
// @param {List<String>} filterOptions — confirmed at Gate 2

/// Status filter options for <Entity> list
/// Generated from Gate 2 confirmation
const List<String> <entitySnake>StatusOptions = [
  // @FillIn: from Gate 2 confirmed filterOptions
];

/// Default page size for <Entity> list pagination
const int <entitySnake>PageSize = 20;

/// Date format for <Entity> display
const String <entitySnake>DateFormat = 'dd/MM/yyyy HH:mm';
```

---

## 6. File Summary

| File | Max Lines | Must Use | Must NOT Use |
|------|-----------|----------|-------------|
| `bloc/*_bloc.dart` | 300 | `Equatable`, repository injection | Business logic beyond delegation |
| `bloc/*_event.dart` | 150 | `Equatable`, sealed classes | Domain logic |
| `bloc/*_state.dart` | 150 | `Equatable`, sealed classes | UI code |
| `pages/*_page.dart` | **30** | `BlocProvider`, `Scaffold` | Any widget beyond these two |
| `widgets/*_list_view.dart` | 300 | `BlocBuilder`, state switch | Direct data fetching |
| `widgets/*_card.dart` | 200 | `ColorSkin`, `TypoSkin` | `Color(0xFF...)`, `Colors.xxx` |
| `widgets/*_card_shimmer.dart` | 100 | `ShimmerWidget` | Raw shimmer implementation |
| `widgets/*_status_filter_chip.dart` | 150 | `BlocBuilder`, `FilterChip` | Hard-coded colors |
| `constants/*_constants.dart` | 100 | Const declarations | Logic, imports from bloc/pages/widgets |
